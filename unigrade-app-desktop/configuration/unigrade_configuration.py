import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()


# --- DB ---
DB_NAME = os.getenv("DB_NAME", "unigrade.db")


# --- JWT ---
JWT_SECRET = os.getenv("JWT_SECRET", "unigrade_local_secret_key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_DELTA_DAYS = int(os.getenv("JWT_EXP_DELTA_DAYS", 7))
