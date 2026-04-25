"""
Semptify55 - Single Source of Truth Constants
All canonical values, enums, and mappings.
"""

from enum import Enum, auto
from typing import Dict, Set


# ============================================================================
# User Roles
# ============================================================================

class UserRole(str, Enum):
    """User roles in the system."""
    TENANT = "tenant"
    ADVOCATE = "advocate"
    LEGAL = "legal"
    MANAGER = "manager"
    JUDGE = "judge"
    ADMIN = "admin"


ALLOWED_ROLES: Set[str] = {r.value for r in UserRole}

# Role code mapping for user IDs (1-char codes)
ROLE_CODES: Dict[str, str] = {
    "T": UserRole.TENANT.value,
    "A": UserRole.ADMIN.value,
    "M": UserRole.MANAGER.value,
    "V": UserRole.ADVOCATE.value,
    "L": UserRole.LEGAL.value,
    "J": UserRole.JUDGE.value,
}

CODE_TO_ROLE: Dict[str, str] = {v: k for k, v in ROLE_CODES.items()}


# ============================================================================
# Storage Providers
# ============================================================================

class StorageProvider(str, Enum):
    """Supported cloud storage providers."""
    GOOGLE_DRIVE = "google_drive"
    DROPBOX = "dropbox"
    ONEDRIVE = "onedrive"


ALLOWED_PROVIDERS: Set[str] = {p.value for p in StorageProvider}

# Provider code mapping for user IDs (1-char codes)
PROVIDER_CODES: Dict[str, str] = {
    "G": StorageProvider.GOOGLE_DRIVE.value,
    "D": StorageProvider.DROPBOX.value,
    "O": StorageProvider.ONEDRIVE.value,
}

CODE_TO_PROVIDER: Dict[str, str] = {v: k for k, v in PROVIDER_CODES.items()}


# ============================================================================
# Case Types
# ============================================================================

class CaseType(str, Enum):
    """Types of tenant cases."""
    LEASE = "lease"                    # Lease disputes
    DEPOSIT = "deposit"                # Deposit return disputes
    EVICTION = "eviction"              # Eviction defense
    REPAIR = "repair"                  # Repair/maintenance issues
    DISCRIMINATION = "discrimination" # Housing discrimination
    OTHER = "other"                    # Other issues


# ============================================================================
# Case Status
# ============================================================================

class CaseStatus(str, Enum):
    """Status of a case."""
    ACTIVE = "active"      # Case in progress
    RESOLVED = "resolved"  # Successfully resolved
    CLOSED = "closed"      # Closed without resolution
    PENDING = "pending"    # Waiting for action


# ============================================================================
# Document Types
# ============================================================================

class DocumentType(str, Enum):
    """Types of documents in a case."""
    LEASE = "lease"                    # Rental agreement
    RECEIPT = "receipt"                # Payment receipts
    PHOTO = "photo"                    # Photos (condition, damage)
    EMAIL = "email"                    # Email communications
    LETTER = "letter"                  # Physical letters
    NOTICE = "notice"                  # Legal notices
    REPAIR = "repair"                  # Repair requests/records
    RECEIPT_REFUND = "receipt_refund"  # Refund receipts
    OTHER = "other"                    # Uncategorized


# ============================================================================
# Timeline Event Types
# ============================================================================

class TimelineEventType(str, Enum):
    """Types of timeline events."""
    # Lease lifecycle
    LEASE_SIGNED = "lease_signed"
    MOVE_IN = "move_in"
    RENT_PAID = "rent_paid"
    REPAIR_REQUESTED = "repair_requested"
    REPAIR_COMPLETED = "repair_completed"
    
    # End of tenancy
    MOVE_OUT_NOTICE = "move_out_notice"
    MOVE_OUT = "move_out"
    FINAL_WALKTHROUGH = "final_walkthrough"
    
    # Deposit disputes
    DEPOSIT_DEDUCTIONS_SENT = "deposit_deductions_sent"
    DEPOSIT_PARTIAL_RETURN = "deposit_partial_return"
    DEPOSIT_FULL_RETURN = "deposit_full_return"
    DEPOSIT_DEMAND_SENT = "deposit_demand_sent"
    DEPOSIT_SUIT_FILED = "deposit_suit_filed"
    
    # Eviction
    EVICTION_NOTICE = "eviction_notice"
    COURT_HEARING = "court_hearing"
    JUDGMENT = "judgment"
    
    # Manual
    MANUAL = "manual"


# ============================================================================
# Tidbit Categories
# ============================================================================

class TidbitCategory(str, Enum):
    """Categories for tenant tidbits (news/education)."""
    RIGHT = "right"          # Know your rights
    TREND = "trend"          # Market trends
    FUN_FACT = "fun_fact"    # Interesting facts
    WARNING = "warning"      # Scams, red flags
    TIP = "tip"              # Practical tips


# ============================================================================
# Cookie Names
# ============================================================================

COOKIE_USER_ID = "semptify_uid"
COOKIE_SESSION = "semptify_session"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 year


# ============================================================================
# OAuth Constants
# ============================================================================

OAUTH_STATE_TIMEOUT_MINUTES = 15
OAUTH_CALLBACK_PATH = "/auth/{provider}/callback"


# ============================================================================
# Vault Paths (relative to user storage root)
# ============================================================================

VAULT_ROOT = "Semptify55/Vault"
VAULT_DOCUMENTS = f"{VAULT_ROOT}/documents"
VAULT_OVERLAYS = f"{VAULT_ROOT}/.overlays"
VAULT_TIMELINE = f"{VAULT_ROOT}/timeline"
VAULT_TIMELINE_EVENTS_FILE = f"{VAULT_TIMELINE}/events.json"
