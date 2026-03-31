# auth.py - JWT authentication and password hashing utilities (Serverless Optimized)

import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import binascii

SECRET_KEY = os.environ.get("SECRET_KEY", "alumni-nexus-secret-key-change-in-production-2024")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password (passlib pbkdf2 format compatible)"""
    try:
        if hashed_password.startswith("$pbkdf2-sha256$"):
            _, alg, iters, salt_b64, hash_b64 = hashed_password.split("$")
            import base64
            # passlib uses non-standard b64 encoding (padding stripped, +/- replaced with ./ )
            # We map . -> +, / -> /, then pad
            def passlib_b64decode(s):
                pad = b'=' * (-len(s) % 4)
                return base64.b64decode(s.replace('.', '+').encode('ascii') + pad)
            
            salt = passlib_b64decode(salt_b64)
            hash_bytes = passlib_b64decode(hash_b64)
            
            new_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt, int(iters))
            return new_hash == hash_bytes
        else:
            # Fallback simple sha256
            return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    except Exception as e:
        print("Password verify error:", e)
        return False

def get_password_hash(password: str) -> str:
    """Hash a password using pure python sha256 to avoid C extensions on Vercel."""
    # Since we removed passlib to save 100MB on Vercel, we use raw sha256 for new passwords
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token using PyJWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT access token using PyJWT."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
