# memora/services/auth_repo.py
from __future__ import annotations
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import bcrypt
from .supabase_client import supabase

def _first(data: Optional[List[dict]]) -> Optional[dict]:
    return data[0] if (data and len(data) > 0) else None

def create_user(username: str, email: str, password_plain: str) -> Dict[str, Any]:
    pw_hash = bcrypt.hashpw(password_plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        supabase.table("users").insert({
            "username": username,
            "email": email,
            "password_hash": pw_hash,
        }).execute()
    except Exception as e:
        raise ValueError(f"Insert failed: {e}") from e

    try:
        get_res = (
            supabase.table("users")
            .select("id, username, email, created_at")
            .eq("email", email)
            .execute()
        )
    except Exception as e:
        raise ValueError(f"Insert succeeded, but fetch failed: {e}") from e

    row = _first(get_res.data)
    if not row:
        raise ValueError("User insert succeeded but no row returned. Check RLS/keys/constraints.")
    return row

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    try:
        res = (
            supabase.table("users")
            .select("id, username, email, password_hash, created_at")
            .eq("email", email)
            .execute()
        )
        return _first(res.data)
    except Exception:
        return None

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    try:
        res = (
            supabase.table("users")
            .select("id, username, email, password_hash, created_at")
            .eq("username", username)
            .execute()
        )
        return _first(res.data)
    except Exception:
        return None

def verify_password(password_plain: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password_plain.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False

def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(48)
    expires_at = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    try:
        supabase.table("sessions").insert({
            "token": token,
            "user_id": user_id,
            "expires_at": expires_at,
        }).execute()
    except Exception as e:
        raise ValueError(f"Failed to create session: {e}") from e
    return token

def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        ses_res = (
            supabase.table("sessions")
            .select("token, user_id, expires_at")
            .eq("token", token)
            .execute()
        )
    except Exception:
        return None

    ses_row = _first(ses_res.data)
    if not ses_row:
        return None

    try:
        if ses_row.get("expires_at"):
            expires = datetime.fromisoformat(ses_row["expires_at"].replace("Z", "+00:00"))
            if datetime.now(timezone.utc) > expires:
                supabase.table("sessions").delete().eq("token", token).execute()
                return None
    except Exception:
        pass

    try:
        user_res = (
            supabase.table("users")
            .select("id, username, email, created_at")
            .eq("id", ses_row["user_id"])
            .execute()
        )
        return _first(user_res.data)
    except Exception:
        return None

def delete_session(token: str) -> None:
    try:
        supabase.table("sessions").delete().eq("token", token).execute()
    except Exception:
        pass
