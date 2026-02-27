import secrets
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from vars import FREE_LIMIT, AD_EXPIRY_HOURS, DOMAIN
from Database.userdb import users, ad_sessions, videos

async def handle_video(client, query):
    user_id = query.from_user.id
    video_id = query.data.split("_")[1]

    user = await users.find_one({"user_id": user_id})
    if not user:
        await users.insert_one({
            "user_id": user_id,
            "is_premium": False,
            "videos_used": 0
        })
        user = await users.find_one({"user_id": user_id})

    if user.get("is_premium"):
        video = await videos.find_one({"_id": video_id})
        await client.send_video(user_id, video["file_id"])
        return

    if user["videos_used"] < FREE_LIMIT:
        video = await videos.find_one({"_id": video_id})
        await client.send_video(user_id, video["file_id"])
        await users.update_one({"user_id": user_id}, {"$inc": {"videos_used": 1}})
        return

    session = await ad_sessions.find_one({"user_id": user_id})

    if session and datetime.utcnow() < session["expires_at"]:
        await ad_sessions.delete_one({"_id": session["_id"]})
        await users.update_one({"user_id": user_id}, {"$set": {"videos_used": 0}})
        video = await videos.find_one({"_id": video_id})
        await client.send_video(user_id, video["file_id"])
        await users.update_one({"user_id": user_id}, {"$inc": {"videos_used": 1}})
        return

    await query.message.reply(
        "🚫 Free limit reached. Watch ad to unlock next 5 videos.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Watch Ad", callback_data="watch_ad")]
        ])
    )


async def handle_watch_ad(client, query):
    user_id = query.from_user.id

    token = secrets.token_hex(16)
    expires_at = datetime.utcnow() + timedelta(hours=AD_EXPIRY_HOURS)

    await ad_sessions.delete_many({"user_id": user_id})
    await ad_sessions.insert_one({
        "user_id": user_id,
        "token": token,
        "expires_at": expires_at
    })

    deep_link = f"{DOMAIN}?start={token}"

    await query.message.reply(f"Complete the ad and return:\n\n{deep_link}")
