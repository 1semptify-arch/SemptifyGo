"""
User ID Generation and Parsing
Format: <provider_code><role_code><random_8chars>
Example: GT7x9kM2pQ = Google + Tenant + random
"""

import secrets
import re
from typing import Optional, Tuple

from app.constants import (
    PROVIDER_CODES, ROLE_CODES,
    CODE_TO_PROVIDER, CODE_TO_ROLE,
    ALLOWED_PROVIDERS, ALLOWED_ROLES
)


def generate_user_id(provider: str, role: str) -> str:
    """Generate new user ID encoding provider and role."""
    # Validate inputs
    if provider not in ALLOWED_PROVIDERS:
        raise ValueError(f"Invalid provider: {provider}")
    if role not in ALLOWED_ROLES:
        raise ValueError(f"Invalid role: {role}")
    
    # Get codes
    provider_code = CODE_TO_PROVIDER.get(provider)
    role_code = CODE_TO_ROLE.get(role)
    
    if not provider_code or not role_code:
        raise ValueError(f"Missing code mapping for provider={provider}, role={role}")
    
    # Generate 8 random alphanumeric characters
    random_part = secrets.token_urlsafe(6)[:8]  # 8 chars, URL-safe
    
    return f"{provider_code}{role_code}{random_part}"


def parse_user_id(user_id: str) -> Tuple[Optional[str], Optional[str], str]:
    """Parse user ID into (provider, role, random_part)."""
    if not user_id or len(user_id) < 10:
        return None, None, ""
    
    provider_code = user_id[0].upper()
    role_code = user_id[1].upper()
    random_part = user_id[2:]
    
    provider = PROVIDER_CODES.get(provider_code)
    role = ROLE_CODES.get(role_code)
    
    return provider, role, random_part


def get_provider_from_user_id(user_id: str) -> Optional[str]:
    """Extract provider from user ID."""
    provider, _, _ = parse_user_id(user_id)
    return provider


def get_role_from_user_id(user_id: str) -> Optional[str]:
    """Extract role from user ID."""
    _, role, _ = parse_user_id(user_id)
    return role


def is_valid_user_id(user_id: str) -> bool:
    """Check if user ID has valid format."""
    if not user_id or len(user_id) < 10:
        return False
    
    provider, role, random_part = parse_user_id(user_id)
    
    if not provider or provider not in ALLOWED_PROVIDERS:
        return False
    
    if not role or role not in ALLOWED_ROLES:
        return False
    
    # Random part should be alphanumeric
    if not re.match(r'^[a-zA-Z0-9_-]+$', random_part):
        return False
    
    return True
