from fastapi import APIRouter, HTTPException
from backend.models.schemas import AdminRegister, AdminLogin, AdminInfo
from datetime import datetime
import re
import uuid
import hashlib
from backend.data_store import data_store

router = APIRouter(prefix="/admin", tags=["admin"])
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")

def _hash_pw(p: str) -> str:
    salt = "uvs_salt_v1"  # replace with env-based salt later
    return hashlib.sha256((salt + p).encode("utf-8")).hexdigest()

@router.post("/register")
async def register_admin(payload: AdminRegister):
    if not USERNAME_RE.match(payload.username):
        raise HTTPException(status_code=400, detail="Username must be 3-32 chars: letters, numbers, underscore only")
    existing = await data_store.get_admin_by_username(payload.username)  # type: ignore[attr-defined]
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", payload.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    pw_hash = _hash_pw(payload.password)
    dob_iso = getattr(payload.dob, "isoformat", lambda: payload.dob)()
    created = await data_store.create_admin(payload.username, payload.name, payload.email, dob_iso, pw_hash)  # type: ignore[attr-defined]
    if not created:
        raise HTTPException(status_code=409, detail="Username already exists")
    return {"ok": True, "admin": AdminInfo(username=payload.username, name=payload.name, email=payload.email, dob=payload.dob, created_at=datetime.utcnow())}

@router.post("/login")
async def login_admin(payload: AdminLogin):
    record = await data_store.get_admin_by_username(payload.username)  # type: ignore[attr-defined]
    if not record or record.get("password_hash") != _hash_pw(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Issue simple session token (placeholder). Replace with JWT.
    token = f"tok_{payload.username}_{uuid.uuid4().hex[:12]}"
    return {"ok": True, "token": token, "admin": {"username": payload.username, "name": record.get("name")}}

@router.get("/me")
async def me(username: str):
    record = await data_store.get_admin_by_username(username)  # type: ignore[attr-defined]
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return {"username": username, "name": record.get("name"), "email": record.get("email")}


@router.get("/violations")
async def get_violations(limit: int = 50):
    try:
        items = await data_store.get_violations(limit)
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_admin_logs(username: str, limit: int = 100):
    try:
        items = await data_store.get_admin_logs(username, limit)  # type: ignore[attr-defined]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notifications")
async def get_notifications(limit: int = 50):
    try:
        items = await data_store.get_notifications(limit)
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/violations")
async def clear_violations():
    """Clear all stored violations and related notifications."""
    try:
        deleted = await data_store.clear_violations()  # type: ignore[attr-defined]
        return {"deleted": deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
