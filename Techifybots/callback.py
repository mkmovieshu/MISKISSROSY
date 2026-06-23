from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from vars import DATABASE_CHANNEL_ID
from database.maindb import mdb
import random, asyncio

async def handle_video(client, query):
    user_id = query.from_user.id
    user = await mdb.get_user(user_id)
    plan = user.get("plan", "free")
    videos = await mdb.get_all_videos() if plan == "prime" else await mdb.get_free_videos()
    
    if not videos:
        await query.message.reply("No videos available")
        return
    
    random_video = random.choice(videos)
    try:
        caption = "**Miss Kiss Bot** 🦋\n\n⚠️ Auto delete in 5 mins\n\n💾 Save to Saved Messages!"
        dy = await client.copy_message(
            chat_id=user_id,
            from_chat_id=DATABASE_CHANNEL_ID,
            message_id=random_video["video_id"],
            caption=caption
        )
        await mdb.increment_daily_count(user_id)
        await asyncio.sleep(300)
        try:
            await dy.delete()
        except:
            pass
    except Exception as e:
        await query.message.reply(f"❌ Error: {str(e)[:100]}")

async def handle_watch_ad(client, query):
    await handle_video(client, query)
