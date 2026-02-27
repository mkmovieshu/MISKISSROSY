import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "prime_zone")

FREE_LIMIT = 5
AD_EXPIRY_HOURS = 12

DOMAIN = os.getenv("DOMAIN")  # https://t.me/YourBot
