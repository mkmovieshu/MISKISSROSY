import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

FREE_LIMIT = int(os.getenv("FREE_LIMIT", 5))
AD_EXPIRY_HOURS = int(os.getenv("AD_EXPIRY_HOURS", 12))

DOMAIN = os.getenv("DOMAIN")
