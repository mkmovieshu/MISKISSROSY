import os

# ==================== Telegram API ====================
API_ID = int(os.getenv("API_ID", "20990520"))
API_HASH = os.getenv("API_HASH", "714a70d62fc73bf8ec1a5d38adf8f198")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ==================== Database ====================
MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_CHANNEL_ID = int(os.getenv("DATABASE_CHANNEL_ID", "-1004379752997"))
LOG_CHNL = int(os.getenv("LOG_CHNL", "-1003532325859"))

# ==================== Admin & Settings ====================
ADMIN_ID = int(os.getenv("ADMIN_ID", "8185007347"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "mkadmin_sir")  # Without @

# ==================== Features ====================
IS_FSUB = bool(os.environ.get("FSUB", True))
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1001986358286").split()))

# ==================== Video Settings ====================
FREE_LIMIT = 5  # ఈరోజు free users చూడగలిగిన videos count
FREE_VIDEO_DURATION = int(os.getenv("FREE_VIDEO_DURATION", "240"))  # 4 minutes
AD_VIDEOS_REWARD = 5  # Ad చూసిన తర్వాత bonus videos
AD_EXPIRY_HOURS = 24  # Ad token validity

# ==================== Ad System ====================
AD_LINK = os.getenv("AD_LINK", "")  # మీ Monetag shortlink
SHORTENER_URL = os.getenv("SHORTENER_URL", "")  # shorturllink, xtz.in, api.shareus.io, etc.
SHORTENER_API = os.getenv("SHORTENER_API", "")  # Shortener API key

# ==================== Misc ====================
PICS = (os.environ.get("PICS", "")).split()
DOMAIN = os.getenv("DOMAIN")  # https://t.me/YourBot
DATABASE_CHANNEL_LOG = int(os.getenv("DATABASE_CHANNEL_LOG", "-1003532325859"))
