# memora/services/supabase_client.py
from __future__ import annotations
import os
from functools import lru_cache
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

def _get_url_and_key():
    url = os.getenv("SUPABASE_URL", "").strip()
    key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY") or "").strip()
    return url, key

@lru_cache(maxsize=1)
def get_client() -> Client:
    url, key = _get_url_and_key()
    if not url or not key:
        raise RuntimeError(
        )
    return create_client(url, key)
