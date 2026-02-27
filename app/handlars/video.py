from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from app.database import users_col, videos_col, ad_sessions_col
from app.config import FREE_LIMIT


@Client.on_callback_query(filters.regex("^video_"))
async def video_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    video_id = query.data.split("_")[1]

    user = await users_col.find_one({"user_id": user_id})

    if user.get("is_premium"):
        video = await videos_col.find_one({"_id": video_id})
        await client.send_video(user_id, video["file_id"])
        return

    if user["videos_used"] < FREE_LIMIT:
        video = await videos_col.find_one({"_id": video_id})
        await client.send_video(user_id, video["file_id"])

        await users_col.update_one(
            {"user_id": user_id},
            {"$inc": {"videos_used": 1}}
        )
        return

    session = await ad_sessions_col.find_one({"user_id": user_id})

    if session and datetime.utcnow() < session["expires_at"]:
        await ad_sessions_col.delete_one({"_id": session["_id"]})
        await users_col.update_one(
            {"user_id": user_id},
            {"$set": {"videos_used": 0}}
        )

        video = await videos_col.find_one({"_id": video_id})
        await client.send_video(user_id, video["file_id"])

        await users_col.update_one(
            {"user_id": user_id},
            {"$inc": {"videos_used": 1}}
        )
        return

    await query.message.reply(
        "🚫 You reached free limit.\nWatch ad to unlock next 5 videos.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Watch Ad", callback_data="watch_ad")]
        ])
    )
