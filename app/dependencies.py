"""
FastAPI Dependencies
"""

from typing import Optional, Annotated

from fastapi import Depends, HTTPException, status, Cookie, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import get_settings
from app.constants import COOKIE_USER_ID, COOKIE_SESSION
from app.core.security import decode_access_token
from app.core.user_id import is_valid_user_id, get_role_from_user_id, get_provider_from_user_id


security_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    semptify_session: Optional[str] = Cookie(None, alias=COOKIE_SESSION),
    semptify_uid: Optional[str] = Cookie(None, alias=COOKIE_USER_ID),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
) -> Optional[dict]:
    """
    Get current user from session cookie or Authorization header.
    Returns user dict or None if not authenticated.
    """
    # Try JWT from cookie first
    if semptify_session:
        payload = decode_access_token(semptify_session)
        if payload:
            return {
                "user_id": payload.get("sub"),
                "role": payload.get("role"),
                "provider": payload.get("provider"),
                "session_id": payload.get("jti"),
            }
    
    # Try JWT from Authorization header
    if credentials:
        payload = decode_access_token(credentials.credentials)
        if payload:
            return {
                "user_id": payload.get("sub"),
                "role": payload.get("role"),
                "provider": payload.get("provider"),
                "session_id": payload.get("jti"),
            }
    
    # Try user ID cookie (indicates storage-connected user)
    if semptify_uid and is_valid_user_id(semptify_uid):
        return {
            "user_id": semptify_uid,
            "role": get_role_from_user_id(semptify_uid),
            "provider": get_provider_from_user_id(semptify_uid),
            "session_id": None,
        }
    
    return None


async def require_user(
    user: Annotated[Optional[dict], Depends(get_current_user)]
) -> dict:
    """Require authenticated user. Raises 401 if not authenticated."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def require_role(role: str):
    """Dependency factory for requiring specific role."""
    async def _check_role(
        user: Annotated[dict, Depends(require_user)]
    ) -> dict:
        if user.get("role") != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' required",
            )
        return user
    return _check_role


# Aliases for cleaner imports
get_current_user_optional = get_current_user
