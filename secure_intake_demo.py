"""
Secure Intake API - Demonstration Artifact

This file illustrates a minimal but production-conscious FastAPI structure
aligned with regulated healthcare system requirements.

Key Concepts Demonstrated:
- Stateless API design
- Role-Based Access Control (RBAC)
- Field-level encryption abstraction
- Audit logging middleware
- Twelve-factor configuration discipline
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from jose import jwt
from cryptography.fernet import Fernet
import os

# -------------------------
# Configuration (12-Factor)
# -------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
ALGORITHM = "HS256"

cipher = Fernet(ENCRYPTION_KEY)

app = FastAPI(title="Secure Intake API Demo")


# -------------------------
# Domain Models
# -------------------------

class User(BaseModel):
    id: int
    role: str


class ClientCreate(BaseModel):
    full_name: str
    ssn: str
    date_of_birth: str
    address: str


# -------------------------
# Authentication
# -------------------------

def create_access_token(user: User):
    payload = {
        "sub": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user():
    """
    Stub for authentication dependency.
    In production, this would decode JWT and validate signature.
    """
    return User(id=1, role="CaseWorker")


# -------------------------
# Authorization (RBAC)
# -------------------------

def require_role(allowed_roles: List[str]):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Unauthorized")
        return user
    return wrapper


# -------------------------
# Encryption Abstraction
# -------------------------

def encrypt_field(value: str) -> str:
    return cipher.encrypt(value.encode()).decode()


def decrypt_field(value: str) -> str:
    return cipher.decrypt(value.encode()).decode()


# -------------------------
# Audit Logging Middleware
# -------------------------

@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    response = await call_next(request)

    log_entry = {
        "path": request.url.path,
        "method": request.method,
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": response.status_code
    }

    # In production this would go to structured logging system
    safe_log = redact_pii(log_entry)
print(safe_log)

    return response


# -------------------------
# Routes
# -------------------------

@app.post("/clients")
async def create_client(
    payload: ClientCreate,
    user: User = Depends(require_role(["Admin", "CaseWorker"]))
):
    encrypted_ssn = encrypt_field(payload.ssn)

    # Simulated DB insert
    client_record = {
        "id": 123,
        "full_name": payload.full_name,
        "encrypted_ssn": encrypted_ssn,
        "created_by": user.id,
        "created_at": datetime.utcnow().isoformat()
    }

    return {
        "message": "Client created",
        "client_id": client_record["id"]
    }


# -------------------------
# PII Redaction Utility
# -------------------------

def redact_pii(data: dict) -> dict:
    redacted = data.copy()
    if "ssn" in redacted:
        redacted["ssn"] = "***REDACTED***"
    return redacted
