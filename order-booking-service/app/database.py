import os

from dotenv import load_dotenv
from supabase import Client, create_client

from app.utils.logger import logger  # Import your logger

load_dotenv()

SUPABASE_URI = os.getenv("SUPABASE_URI")
SUPABASE_PROJECT_KEY = os.getenv("SUPABASE_PROJECT_KEY")

if not SUPABASE_URI or not SUPABASE_URI:
    logger.error("Supabase URL or Key is missing in environment variables")
    raise ValueError("Supabase URL and Key must be set in the environment variables")

try:
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URI, SUPABASE_PROJECT_KEY)
    logger.info("Successfully connected to Supabase")
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {e}")
    raise RuntimeError("Could not connect to Supabase") from e
