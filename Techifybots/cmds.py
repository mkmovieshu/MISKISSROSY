from pyrogram import Client, filters
from pyrogram.types import *
from vars import *
from database.maindb import mdb
from database.userdb import udb
from datetime import datetime
import pytz, random, asyncio
from .fsub import get_fsub
from Script import text

async def get_updated_limits():
        global FREE_LIMIT, PRIME_LIMIT
        limits = await mdb.get_global_limits()
        FREE_LIMIT = limits["free_limit"]
        PRIME_LIMIT = limits["prime_limit"]
        return limits

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    if await udb.is_user_banned(message.from_user.id):
        await message.reply("**🚫 You are banned from using this bot**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support 🧑‍💻", url=f"https://t.me/{ADMIN_USERNAME}")]]))
        return
    if IS_FSUB and not await get_fsub(client, message):return
    if await udb.get_user(message.from_user.id) is None:
        await udb.addUser(message.from_user.id, message.from_user.first_name)
        bot = await client.get_me()
        await client.send_message(
            LOG_CHNL,
            text.LOG.format(
                message.from_user.id,
                getattr(message.from_user, "dc_id", "N/A"),
                message.from_user.first_name or "N/A",
                f"@{message.from_user.username}" if message.from_user.username else "N/A",
                bot.username
            )
        )
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=text.START.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🍿 𝖡𝗎𝗒 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 🍾", callback_data="pro")],
            [InlineKeyboardButton("ℹ️ 𝖠𝖻𝗈𝗎𝗍", callback_data="about"),
             InlineKeyboardButton("📚 𝖧𝖾𝗅𝗉", callback_data="help")] 
        ])
    )

@Client.on_message(filters.command("watch") & filters.private)
async def watch_command(client: Client, message: Message):
    # /watch కూడా /getvideos లాగే పని చేస్తుంది
    await send_random_video(client, message)

@Client.on_message(filters.command("getvideos") & filters.private)
async def send_random_video(client: Client, message: Message):
    if await udb.is_user_banned(message.from_user.id):
        await message.reply("**🚫 You are banned from using this bot**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support 🧑‍💻", url=f"https://t.me/{ADMIN_USERNAME}")]]))
        return
    limits = await get_updated_limits()
    if limits.get('maintenance', False):
        await message.reply_text("**🛠️ Bot Under Maintenance — Back Soon!**")
        return
    if IS_FSUB and not await get_fsub(client, message):return
    user_id = message.from_user.id
    user = await mdb.get_user(user_id)
    plan = user.get("plan", "free")
    if plan == "prime":
        videos = await mdb.get_all_videos()
    else:
        videos = await mdb.get_free_videos()
    if not videos:
        await message.reply_text("No videos available at the moment.")
        return
    random_video = random.choice(videos)
    daily_count = user.get("daily_count", 0)
    daily_limit = user.get("daily_limit", FREE_LIMIT)
    if daily_count > daily_limit:
        await message.reply_text(f"**🚫 You've reached your daily limit of {daily_limit} videos.\n\n>Limit will reset every day at 5 AM (IST).**")
    else:
        try:
            limits = await get_updated_limits()
            total_limit = limits.get("free_limit", FREE_LIMIT) if plan != "prime" else limits.get("prime_limit", 50)
            loading_msg = await message.reply_text(
                f"🎬 వీడియో లోడ్ అవుతోంది...\n(ఈరోజు మీరు చూసినవి: {daily_count + 1}/{total_limit})"
            )
            caption_text = "<b><blockquote>🔞 Powered by: Miss Kiss Bot</blockquote>\n\n⚠️ This file will auto delete in 5 minutes!\n\n💾 Please <b>save it in your Saved Messages</b> or <b>forward it elsewhere</b> to keep it safe! 🔐</b>"
            video_id = random_video["video_id"]
            dy = await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=DATABASE_CHANNEL_ID,
                message_id=video_id,
                caption=caption_text)
            await mdb.increment_daily_count(user_id)
            try:
                await loading_msg.delete()
            except:
                pass
            await asyncio.sleep(300)
            try:
                await dy.delete()
            except:
                pass
        except Exception as e:
            print(f"Error sending video: {e}")
            err_msg = str(e)
            if "MESSAGE_ID_INVALID" in err_msg or "message not found" in err_msg.lower():
                # Video DB లో ఉంది కానీ channel లో లేదు — remove చేయి
                await mdb.delete_video_by_id(random_video["video_id"])
                await message.reply_text("⚠️ Video not found, please try again with /watch")
            elif "CHAT_ADMIN_REQUIRED" in err_msg or "forbidden" in err_msg.lower():
                await message.reply_text("❌ Bot కి Database Channel లో admin access లేదు. Admin ని contact చేయండి.")
            else:
                await message.reply_text(f"❌ Video పంపడం failed. దయచేసి మళ్ళీ try చేయండి.\n\n`{err_msg[:100]}`")
