"""
Ad Watch Commands with Shortener Support
"""
from pyrogram import Client, filters
from pyrogram.types import *
from vars import AD_LINK, FREE_LIMIT, AD_VIDEOS_REWARD, ADMIN_USERNAME, SHORTENER_URL
from database.maindb import mdb
from database.adsession import addb
from shortener import get_short_link, create_ad_short_link

@Client.on_message(filters.command("watch") & filters.private)
async def watch_ad_command(client: Client, message: Message):
    """User ad చూద్దానని offer చేయడానికి"""
    user_id = message.from_user.id
    user = await mdb.get_user(user_id)
    
    # Session create చేయి
    session = await addb.create_session(user_id, AD_VIDEOS_REWARD)
    token = session['token']
    
    # Bot details get
    bot = await client.get_me()
    
    # Verification link create చేయి
    verify_link = f"https://t.me/{bot.username}?start=av_{token}"
    
    # Short link create చేయి (if shortener configured)
    short_verify_link = await create_ad_short_link(bot.username, token)
    if short_verify_link != verify_link:
        verify_link = short_verify_link  # Use shortened version if available
    
    # AD link (shortener used if available)
    ad_url = AD_LINK if AD_LINK else "https://example.com"
    if SHORTENER_URL and AD_LINK:
        ad_url = await get_short_link(AD_LINK)  # Short the ad link too
    
    await message.reply_text(
        f"**🎬 యాడ్ చూసి {AD_VIDEOS_REWARD} FREE videos పొందండి!**\n\n"
        f"**📺 How to earn:**\n"
        f"**Step 1:** 'AD చూడండి' button నొక్కండి\n"
        f"**Step 2:** AD పూర్తయిన తర్వాత 'Verify' చేయండి\n"
        f"**Step 3:** మరో {AD_VIDEOS_REWARD} videos unlock! 🎉\n\n"
        f"**⏱️ Link 24 hours valid | Every day reset**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📺 AD చూడండి", url=ad_url)],
            [InlineKeyboardButton("✅ Verify చేయండి", url=verify_link)],
            [InlineKeyboardButton("👑 Premium కొనండి", callback_data="pro")]
        ])
    )

@Client.on_message(filters.command("start") & filters.private)
async def ad_verify_start(client: Client, message: Message):
    """
    /start av_TOKEN ద్వారా ad verify చేస్తుంది
    """
    args = message.text.split()
    
    # Ad verify parameter ఉందో చెక్
    if len(args) > 1 and args[1].startswith("av_"):
        token = args[1].replace("av_", "")
        user_id = message.from_user.id
        
        # Token verify చేయి
        valid = await addb.verify_session(user_id, token)
        
        if valid:
            # Reward videos get చేయి
            reward = await addb.get_reward(user_id, token)
            user = await mdb.get_user(user_id)
            
            # Daily limit increase చేయి
            old_limit = user.get("daily_limit", FREE_LIMIT)
            new_limit = old_limit + reward
            
            await mdb.update_user(user_id, {
                "daily_limit": new_limit
            })
            
            await message.reply_text(
                f"**✅ AD Verified Successfully! 🎉**\n\n"
                f"**{reward} NEW videos unlocked!**\n\n"
                f"మీ daily limit: {old_limit} → **{new_limit}** videos\n\n"
                f"/watch టైప్ చేసి videos చూడండి! 🎬",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎬 Watch Video", callback_data="watch_video")]
                ])
            )
            return
        else:
            await message.reply_text(
                f"**❌ Token Invalid లేదా Expired!**\n\n"
                f"/watch టైప్ చేసి కొత్త ad link తీసుకోండి.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📺 Get New Link", callback_data="get_ad_link")]
                ])
            )
            return
    
    # Normal start command
    if await mdb.get_user(message.from_user.id) is None:
        await mdb.add_user(message.from_user.id)
    
    await message.reply_text(
        f"**Hey {message.from_user.first_name}! 👋**\n\n"
        f"**MISS KISS BOT - ఉచిత videos చూడండి!**\n\n"
        f"/watch - Videos చూడండి 🎬\n"
        f"/plans - Premium plans 👑",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Watch", callback_data="watch_video"), 
             InlineKeyboardButton("👑 Premium", callback_data="pro")]
        ])
    )
