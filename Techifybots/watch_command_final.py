"""
Modified /watch command - Ad System with Shortener
"""
from pyrogram import Client, filters
from pyrogram.types import *
from vars import FREE_LIMIT, AD_VIDEOS_REWARD, ADMIN_USERNAME, DATABASE_CHANNEL_ID, SHORTENER_URL
from database.maindb import mdb
from database.userdb import udb
from database.adsession import addb
from shortener import get_short_link, create_ad_short_link
import random, asyncio

@Client.on_message(filters.command("watch") & filters.private)
async def watch_command(client: Client, message: Message):
    """Video చూడండి - Complete Ad System"""
    user_id = message.from_user.id
    
    # User banned check
    if await udb.is_user_banned(user_id):
        await message.reply_text(
            "**🚫 You are banned from using this bot**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Support 🧑‍💻", url=f"https://t.me/{ADMIN_USERNAME}")]
            ])
        )
        return
    
    # Maintenance check
    limits = await mdb.get_global_limits()
    if limits.get('maintenance', False):
        await message.reply_text("**🛠️ Bot Under Maintenance — Back Soon!**")
        return
    
    # User data get
    user = await mdb.get_user(user_id)
    plan = user.get("plan", "free")
    daily_count = user.get("daily_count", 0)
    daily_limit = user.get("daily_limit", FREE_LIMIT)
    
    # ============ LIMIT CHECK ============
    if daily_count >= daily_limit:
        # Ad session create చేయి
        session = await addb.create_session(user_id, AD_VIDEOS_REWARD)
        
        # Bot username get
        bot = await client.get_me()
        
        # Verify link create + short
        verify_link = f"https://t.me/{bot.username}?start=av_{session['token']}"
        short_verify_link = await create_ad_short_link(bot.username, session['token'])
        
        # Use shortened link if available
        final_verify_link = short_verify_link if short_verify_link != verify_link else verify_link
        
        await message.reply_text(
            f"**🚫 మీ ఈరోజటి {daily_limit} videos limit అయిపోయింది!**\n\n"
            f"**📺 AD చూసి {AD_VIDEOS_REWARD} मरा videos పొందండి:**\n\n"
            f"**Step 1:** 'AD చూడండి' button నొక్కండి\n"
            f"**Step 2:** AD పూర్తయిన తర్వాత 'Verify' చేయండి\n"
            f"**Step 3:** మరో {AD_VIDEOS_REWARD} videos unlock! 🎉\n\n"
            f"**⏱️ Link 24 hours valid | Daily reset: 5 AM IST**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📺 AD చూడండి", url="https://example.com")],  # Your AD_LINK
                [InlineKeyboardButton("✅ Verify చేయండి", url=final_verify_link)],
                [InlineKeyboardButton("👑 Premium కొనండి", callback_data="pro")]
            ])
        )
        return
    
    # ============ VIDEO SEND ============
    videos = await mdb.get_all_videos() if plan == "prime" else await mdb.get_free_videos()
    
    if not videos:
        await message.reply_text("**❌ Videos Available లేవు! తర్వాత try చేయండి.**")
        return
    
    random_video = random.choice(videos)
    
    try:
        loading_msg = await message.reply_text(
            f"🎬 వీడియో లోడ్ అవుతోంది...\n"
            f"(ఈరోజు చూశారు: {daily_count + 1}/{daily_limit})"
        )
        
        caption = (
            f"**Miss Kiss Bot** 🦋\n\n"
            f"⚠️ Auto delete in 5 minutes\n\n"
            f"💾 Save to Saved Messages!"
        )
        
        dy = await client.copy_message(
            chat_id=user_id,
            from_chat_id=DATABASE_CHANNEL_ID,
            message_id=random_video["video_id"],
            caption=caption
        )
        
        await mdb.increment_daily_count(user_id)
        
        try:
            await loading_msg.delete()
        except:
            pass
        
        # 5 minutes తర్వాత auto delete
        await asyncio.sleep(300)
        try:
            await dy.delete()
        except:
            pass
            
    except Exception as e:
        err = str(e)
        if "MESSAGE_ID_INVALID" in err:
            await mdb.delete_video_by_id(random_video["video_id"])
            await message.reply_text("⚠️ Video not found, try again with /watch")
        elif "CHAT_ADMIN" in err:
            await message.reply_text("❌ Bot admin access లేదు database channel లో!")
        else:
            await message.reply_text(f"❌ Error: {err[:80]}")
