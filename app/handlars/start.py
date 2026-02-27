from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from app.database import users_col, ad_sessions_col


@Client.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    args = message.command

    user = await users_col.find_one({"user_id": user_id})
    if not user:
        await users_col.insert_one({
            "user_id": user_id,
            "is_premium": False,
            "videos_used": 0
        })

    if len(args) > 1:
        token = args[1]

        session = await ad_sessions_col.find_one({"token": token})

        if not session:
            await message.reply("❌ Invalid token.")
            return

        if session["user_id"] != user_id:
            await message.reply("❌ This token is not for you.")
            return

        if datetime.utcnow() > session["expires_at"]:
            await ad_sessions_col.delete_one({"_id": session["_id"]})
            await message.reply("❌ Token expired. Watch ad again.")
            return

        await message.reply("✅ Ad verified. Try accessing video again.")
        return

    await message.reply("Welcome to Prime Zone Bot.")
