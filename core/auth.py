import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pydantic import BaseModel

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: Missing SUPABASE_URL or SUPABASE_KEY in .env")
    supabase = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class User(BaseModel):
    id: str
    email: str
    is_pro: bool = False

def get_current_user_from_token(token: str) -> User:
    if not supabase:
        return None
    try:
        res = supabase.auth.get_user(token)
        if res and res.user:
            is_pro = res.user.user_metadata.get('is_pro', False)
            return User(id=res.user.id, email=res.user.email, is_pro=is_pro)
    except Exception as e:
        print(f"Token validation error: {e}")
    return None

# Dummy functions to avoid import errors in other files
def get_db():
    yield None

def verify_password(plain, hashed):
    pass

def get_password_hash(password):
    pass

def create_access_token(data, expires_delta=None):
    pass

def decode_access_token(token):
    pass
