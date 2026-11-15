import os
import psycopg

from dotenv import load_dotenv

load_dotenv()

# Neon cloud provider hosting the PostgreSQL database
NEON_URL = os.getenv("NEON_URL")

if not NEON_URL:
    raise RuntimeError("NEON_URL was not found in the .env file.")

def get_connection():
    return psycopg.connect(NEON_URL, sslmode="require")