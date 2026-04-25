"""
Semptify55 - Configuration
Pydantic Settings for environment-based configuration.
"""

from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    app_name: str = "Semptify55"
    app_version: str = "0.1.0"
    environment: str = Field(default="development", pattern="^(development|staging|production)$")
    debug: bool = Field(default=False)
    
    # Security
    secret_key: str = Field(default="change-me-in-production")
    security_mode: str = Field(default="open", pattern="^(open|enforced)$")
    access_token_expire_minutes: int = Field(default=60 * 24 * 7)  # 7 days
    
    # Database
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/semptify55")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")
    
    # CORS
    cors_origins: str = Field(default="http://localhost:8000,http://localhost:3000")
    
    @field_validator("cors_origins")
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        return [origin.strip() for origin in v.split(",")]
    
    # OAuth - Google Drive
    google_drive_client_id: Optional[str] = None
    google_drive_client_secret: Optional[str] = None
    
    # OAuth - Dropbox
    dropbox_app_key: Optional[str] = None
    dropbox_app_secret: Optional[str] = None
    
    # OAuth - OneDrive
    onedrive_client_id: Optional[str] = None
    onedrive_client_secret: Optional[str] = None
    
    # Vault Paths
    semptify_root: str = "Semptify55"
    vault_documents: str = "Vault/documents"
    vault_overlays: str = "Vault/.overlays"
    vault_timeline: str = "Vault/timeline"
    
    # Admin
    admin_email: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
