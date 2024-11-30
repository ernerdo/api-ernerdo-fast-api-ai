import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
jwt_secret: str = os.environ.get("SUPABASE_JWT_SECRET")
jwt_algorithm: str = os.environ.get("SUPABASE_JWT_ALGORITHM")

if not all([url, key, jwt_secret]):
    raise ValueError("Missing some supabase environment")
    
supabase_client: Client = create_client(url, key)
