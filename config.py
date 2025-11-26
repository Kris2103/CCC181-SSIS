from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

import os

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

if all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST]):
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = None

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY") 

# Initialize the global Supabase client object
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        # Create the Supabase client using the URL and Service Role Key
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")

STORAGE_BUCKET = 'Student_profile' 
SUPABASE_BASE_URL = None

if SUPABASE_URL:
    # This URL is used to construct public links to the files in the 'Student_profile' bucket.
    SUPABASE_BASE_URL = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/"