import os

# Render Environment Variables నుండి డేటా తీసుకుంటుంది
BOT_TOKEN = os.getenv("BOT_TOKEN")
PREMIUM_CHANNEL_ID = int(os.getenv("PREMIUM_CHANNEL_ID", "0"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0")) # కొత్త యూజర్ల వివరాల కోసం
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
FREE_CHANNEL_LINK = os.getenv("FREE_CHANNEL_LINK")
