from vars import *
import time
from pytz import timezone
from datetime import datetime
import os
from pyrogram import Client

# వెబ్ సర్వర్ కోడ్ అవసరం లేదు, అందుకే తీసివేస్తున్నాం

class Bot(Client):
    def __init__(self):
        super().__init__(
            "techifybots",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechifyBots"),
            workers=200,
            sleep_threshold=15
        )
        self.START_TIME = time.time()

    async def start(self):
        # ఇక్కడ ఉన్న web_server() మరియు TCPSite కోడ్ మొత్తాన్ని తీసివేస్తున్నాం
        # ఇది పోర్ట్ ఎర్రర్‌ను నివారిస్తుంది.
        
        await super().start()
        me = await self.get_me()
        print(f"Bot Started as {me.first_name}")
        
        if isinstance(ADMIN_ID, int):
            try:
                await self.send_message(ADMIN_ID, f"**{me.first_name} is started...**")
            except Exception as e:
                print(f"Error sending message to admin: {e}")

        if LOG_CHNL:
            try:
                now = datetime.now(timezone("Asia/Kolkata"))
                msg = (
                    f"**{me.mention} is restarted!**\n\n"
                    f"📅 Date : `{now.strftime('%d %B, %Y')}`\n"
                    f"⏰ Time : `{now.strftime('%I:%M:%S %p')}`\n"
                    f"🌐 Timezone : `Asia/Kolkata`"
                )
                await self.send_message(LOG_CHNL, msg)
            except Exception as e:
                print(f"Error sending to LOG_CHANNEL: {e}")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped.")

bot = Bot()
