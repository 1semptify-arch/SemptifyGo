"""
Simplified Auth Router
OAuth flow: initiate → callback → session cookie
Based on working Semptify5.0, cleaned for 55.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Request, Response, HTTPException, Depends, Query, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.constants import StorageProvider, UserRole, COOKIE_USER_ID, COOKIE_SESSION, COOKIE_MAX_AGE
from app.core.user_id import generate_user_id
from app.core.security import create_access_token, encrypt_data
from app.db import get_db
from app.dependencies import require_user
from app.services.oauth import (
    generate_oauth_state,
    verify_oauth_state,
    get_auth_url,
    exchange_code,
)
from app.models import User, Session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/{provider}/initiate")
async def initiate_oauth(
    provider: str,
    role: Optional[str] = "tenant",
    request: Request = None,
):
    """
    Start OAuth flow. Redirects to provider's auth page.
    
    Args:
        provider: google, dropbox, or onedrive
        role: tenant, advocate, legal, etc. (default: tenant)
    """
    # Validate provider
    try:
        provider_enum = StorageProvider(provider.lower().replace("google", "google_drive"))
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
    
    # Generate state
    state = generate_oauth_state(provider_enum)
    
    # Build auth URL with state
    auth_url = get_auth_url(provider_enum, state)
    
    # For development, return JSON with URL
    # For production, redirect directly
    settings = get_settings()
    if settings.environment == "development":
        return {"auth_url": auth_url, "state": state}
    
    return RedirectResponse(url=auth_url)


@router.get("/{provider}/callback")
async def oauth_callback(
    provider: str,
    code: str = Query(...),
    state: str = Query(...),
    request: Request = None,
    response: Response = None,
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth callback. Exchange code for tokens, create user, set session.
    """
    settings = get_settings()
    base_url = str(request.base_url).rstrip("/")
    
    # Verify state
    provider_enum = verify_oauth_state(state)
    if not provider_enum:
        logger.warning("Invalid or expired OAuth state")
        raise HTTPException(status_code=400, detail="Invalid or expired state")
    
    # Exchange code for tokens
    try:
        token_data = await exchange_code(provider_enum, code, base_url)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token exchange failed: {e}")
        raise HTTPException(status_code=400, detail="Failed to complete OAuth")
    
    # Generate user ID (simple: provider code + T for tenant + random)
    user_id = generate_user_id(provider_enum.value, UserRole.TENANT.value)
    
    # Calculate token expiry
    expires_at = datetime.utcnow() + timedelta(seconds=token_data.get("expires_in", 3600))
    
    # Create/update user in DB
    user = await db.get(User, user_id)
    if not user:
        user = User(
            id=user_id,
            provider=provider_enum,
            role=UserRole.TENANT,
        )
        db.add(user)
    
    # Create session
    session = Session(
        user_id=user_id,
        access_token_encrypted=encrypt_data(token_data["access_token"]),
        refresh_token_encrypted=encrypt_data(token_data["refresh_token"]) if token_data.get("refresh_token") else None,
        expires_at=expires_at,
    )
    db.add(session)
    await db.commit()
    
    # Create JWT for session cookie
    jwt_token = create_access_token(
        data={
            "sub": user_id,
            "role": UserRole.TENANT.value,
            "provider": provider_enum.value,
            "session_id": session.id,
        },
        expires_delta=timedelta(days=7),
    )
    
    # Build response with cookies
    redirect_response = RedirectResponse(url="/dashboard")
    
    # Set cookies
    redirect_response.set_cookie(
        key=COOKIE_USER_ID,
        value=user_id,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
    )
    
    redirect_response.set_cookie(
        key=COOKIE_SESSION,
        value=jwt_token,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
    )
    
    logger.info(f"User {user_id} authenticated via {provider_enum.value}")
    
    return redirect_response


@router.post("/logout")
async def logout(
    response: Response,
    semptify_session: Optional[str] = Cookie(None, alias=COOKIE_SESSION),
):
    """Logout: clear cookies."""
    response.delete_cookie(COOKIE_USER_ID)
    response.delete_cookie(COOKIE_SESSION)
    return {"message": "Logged out"}


@router.get("/me")
async def get_current_user_info(
    user: dict = Depends(require_user),
):
    """Get current authenticated user info."""
    return {
        "user_id": user["user_id"],
        "role": user["role"],
        "provider": user["provider"],
    }
