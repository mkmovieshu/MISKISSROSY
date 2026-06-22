import os
API_ID = int(os.getenv("API_ID", "20990520"))
API_HASH = os.getenv("API_HASH", "714a70d62fc73bf8ec1a5d38adf8f198")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_CHANNEL_ID = int(os.getenv("DATABASE_CHANNEL_ID", "-1001986666096"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "8185007347"))
PICS = (os.environ.get("PICS", "")).split()
LOG_CHNL = int(os.getenv("LOG_CHNL", "-1003532325859"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "mkadmin_sir") # Without @
IS_FSUB = bool(os.environ.get("FSUB", True))
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1001986358286").split()))
DATABASE_CHANNEL_LOG = int(os.getenv("DATABASE_CHANNEL_LOG", "-1003532325859"))
FREE_VIDEO_DURATION = int(os.getenv("FREE_VIDEO_DURATION", "240"))

FREE_LIMIT = 5
AD_EXPIRY_HOURS = 12

DOMAIN = os.getenv("DOMAIN")  # https://t.me/YourBot
