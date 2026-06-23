from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from vars import FREE_LIMIT, DATABASE_CHANNEL_ID
from database.maindb import mdb
import random, asyncio

async def handle_video(client, query):
    user_id = query.from_user.id
    user = await mdb.get_user(user_id)
    plan = user.get("plan", "free")

    if plan == "prime":
        videos = await mdb.get_all_videos()
    else:
        videos = await mdb.get_free_videos()

    if not videos:
        await query.message.reply("No videos available at the moment.")
        return

    random_video = random.choice(videos)
    daily_count = user.get("daily_count", 0)
    daily_limit = user.get("daily_limit", FREE_LIMIT)

    if daily_count >= daily_limit:
        await query.message.reply(
            f"**🚫 Daily limit {daily_limit} videos అయిపోయింది.\n\n>రోజూ 5 AM (IST) కి reset అవుతుంది.**"
        )
        return

    try:
        caption_text = "<b><blockquote>Miss Kiss Bot</blockquote>\n\n⚠️ 5 నిమిషాల్లో auto delete అవుతుంది!\n\n💾 Saved Messages లో forward చేసుకోండి!</b>"
        video_id = random_video["video_id"]
        dy = await client.copy_message(
            chat_id=user_id,
            from_chat_id=DATABASE_CHANNEL_ID,
            message_id=video_id,
            caption=caption_text
        )
        await mdb.increment_daily_count(user_id)
        await asyncio.sleep(300)
        try:
            await dy.delete()
        except:
            pass
    except Exception as e:
        err = str(e)
        if "MESSAGE_ID_INVALID" in err:
            await mdb.delete_video_by_id(random_video["video_id"])
            await query.message.reply("⚠️ Video దొరకలేదు, మళ్ళీ try చేయండి.")
        else:
            await query.message.reply(f"❌ Error: {err[:100]}")


async def handle_watch_ad(client, query):
    # Ad system తీసివేయబడింది - నేరుగా video పంపుతోంది
    await handle_video(client, query)
