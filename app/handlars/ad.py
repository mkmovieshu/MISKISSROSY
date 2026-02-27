import secrets
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from app.database import ad_sessions_col
from app.config import AD_EXPIRY_HOURS, DOMAIN


@Client.on_callback_query(filters.regex("^watch_ad$"))
async def watch_ad_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id

    token = secrets.token_hex(16)

    expires_at = datetime.utcnow() + timedelta(hours=AD_EXPIRY_HOURS)

    await ad_sessions_col.delete_many({"user_id": user_id})

    await ad_sessions_col.insert_one({
        "user_id": user_id,
        "token": token,
        "expires_at": expires_at
    })

    deep_link = f"{DOMAIN}?start={token}"

    await query.message.reply(
        f"Watch the ad and return:\n\n{deep_link}"
    )
