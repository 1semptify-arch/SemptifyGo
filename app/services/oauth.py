"""
Simplified OAuth Service
Based on working Semptify5.0 pattern, cleaned for Semptify55.
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import httpx
from fastapi import HTTPException

from app.config import get_settings
from app.constants import StorageProvider

# OAuth state storage (in production, use Redis)
# For Semptify55: simple in-memory with short expiry
_oauth_states: Dict[str, dict] = {}


def generate_oauth_state(provider: StorageProvider) -> str:
    """Generate and store OAuth state token."""
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = {
        "provider": provider.value,
        "created_at": datetime.utcnow(),
    }
    # Clean old states (simple garbage collection)
    _cleanup_old_states()
    return state


def verify_oauth_state(state: str) -> Optional[StorageProvider]:
    """Verify state token and return provider if valid."""
    data = _oauth_states.pop(state, None)
    if not data:
        return None
    
    # Check expiry (15 minutes)
    age = datetime.utcnow() - data["created_at"]
    if age > timedelta(minutes=15):
        return None
    
    return StorageProvider(data["provider"])


def _cleanup_old_states():
    """Remove expired states."""
    now = datetime.utcnow()
    expired = [
        state for state, data in _oauth_states.items()
        if now - data["created_at"] > timedelta(minutes=15)
    ]
    for state in expired:
        _oauth_states.pop(state, None)


# =============================================================================
# Provider Configurations
# =============================================================================

def get_google_auth_url(state: str) -> str:
    """Build Google Drive OAuth URL."""
    settings = get_settings()
    if not settings.google_drive_client_id:
        raise HTTPException(status_code=500, detail="Google Drive not configured")
    
    return (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.google_drive_client_id}"
        "&redirect_uri=/auth/google/callback"
        "&scope=https://www.googleapis.com/auth/drive.file"
        "&response_type=code"
        "&access_type=offline"
        "&prompt=consent"
        f"&state={state}"
    )


def get_dropbox_auth_url(state: str) -> str:
    """Build Dropbox OAuth URL."""
    settings = get_settings()
    if not settings.dropbox_app_key:
        raise HTTPException(status_code=500, detail="Dropbox not configured")
    
    return (
        "https://www.dropbox.com/oauth2/authorize"
        f"?client_id={settings.dropbox_app_key}"
        "&redirect_uri=/auth/dropbox/callback"
        "&response_type=code"
        f"&state={state}"
    )


def get_onedrive_auth_url(state: str) -> str:
    """Build OneDrive OAuth URL."""
    settings = get_settings()
    if not settings.onedrive_client_id:
        raise HTTPException(status_code=500, detail="OneDrive not configured")
    
    return (
        "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
        f"?client_id={settings.onedrive_client_id}"
        "&redirect_uri=/auth/onedrive/callback"
        "&scope=Files.ReadWrite offline_access"
        "&response_type=code"
        f"&state={state}"
    )


def get_auth_url(provider: StorageProvider, state: str) -> str:
    """Get OAuth URL for provider."""
    urls = {
        StorageProvider.GOOGLE_DRIVE: get_google_auth_url,
        StorageProvider.DROPBOX: get_dropbox_auth_url,
        StorageProvider.ONEDRIVE: get_onedrive_auth_url,
    }
    return urls[provider](state)


# =============================================================================
# Token Exchange
# =============================================================================

async def exchange_google_code(code: str, base_url: str) -> Dict[str, Any]:
    """Exchange Google auth code for tokens."""
    settings = get_settings()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": settings.google_drive_client_id,
                "client_secret": settings.google_drive_client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": f"{base_url}/auth/google/callback",
            },
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to exchange code")
    
    data = response.json()
    return {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token"),
        "expires_in": data.get("expires_in", 3600),
    }


async def exchange_dropbox_code(code: str, base_url: str) -> Dict[str, Any]:
    """Exchange Dropbox auth code for tokens."""
    settings = get_settings()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.dropboxapi.com/oauth2/token",
            data={
                "code": code,
                "grant_type": "authorization_code",
                "client_id": settings.dropbox_app_key,
                "client_secret": settings.dropbox_app_secret,
                "redirect_uri": f"{base_url}/auth/dropbox/callback",
            },
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to exchange code")
    
    data = response.json()
    return {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token"),
        "expires_in": data.get("expires_in", 3600),
    }


async def exchange_onedrive_code(code: str, base_url: str) -> Dict[str, Any]:
    """Exchange OneDrive auth code for tokens."""
    settings = get_settings()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            data={
                "client_id": settings.onedrive_client_id,
                "client_secret": settings.onedrive_client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": f"{base_url}/auth/onedrive/callback",
            },
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to exchange code")
    
    data = response.json()
    return {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token"),
        "expires_in": data.get("expires_in", 3600),
    }


async def exchange_code(provider: StorageProvider, code: str, base_url: str) -> Dict[str, Any]:
    """Exchange auth code for tokens."""
    exchangers = {
        StorageProvider.GOOGLE_DRIVE: exchange_google_code,
        StorageProvider.DROPBOX: exchange_dropbox_code,
        StorageProvider.ONEDRIVE: exchange_onedrive_code,
    }
    return await exchangers[provider](code, base_url)
