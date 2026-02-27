from pyrogram import Client
from app.config import BOT_TOKEN, API_ID, API_HASH

app = Client(
    "prime_zone_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

import app.handlers.start
import app.handlers.video
import app.handlers.ad

app.run()
