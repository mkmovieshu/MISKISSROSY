import os
import logging
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import *
import database as db

logging.basicConfig(level=logging.INFO)
app = Flask('')

@app.route('/')
def home(): return "Referral Audio Bot is Live!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args # రిఫరల్ ఐడి కోసం
    
    referred_by = int(args[0]) if args and args[0].isdigit() else None
    is_new = db.add_user(user.id, referred_by)

    if is_new and referred_by:
        try: await context.bot.send_message(chat_id=referred_by, text="🎉 మీ ఫ్రెండ్ జాయిన్ అయ్యారు! మీకు ఒక బోనస్ ఎపిసోడ్ లభించింది.")
        except: pass

    keyboard = [[InlineKeyboardButton(f"🎬 {data['name']}", callback_data=f"select_{key}")] for key, data in SERIES_LIST.items()]
    keyboard.append([InlineKeyboardButton("🔗 నా రిఫరల్ లింక్", callback_data="my_ref")])
    
    await update.message.reply_text(f"నమస్కారం! 🙏\nమీ రిఫరల్ బోనస్: {db.get_user_bonus(user.id)} ఎపిసోడ్లు ఉన్నాయి.\nసిరీస్ ఎంచుకోండి:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith("select_"):
        s_key = query.data.split('_')[-1]
        bonus = db.get_user_bonus(user_id)
        keyboard = [
            [InlineKeyboardButton("🎧 5 ఫ్రీ ఆడియోలు", callback_data=f"free_{s_key}")],
            [InlineKeyboardButton(f"🎁 బోనస్ ఎపిసోడ్ వినండి ({bonus})", callback_data=f"bonus_{s_key}")],
            [InlineKeyboardButton("💎 ప్రీమియం కొనండి", callback_data=f"pay_{s_key}")],
            [InlineKeyboardButton("🔙 వెనక్కి", callback_data="back_to_list")]
        ]
        await query.edit_message_text(f"🎬 **{SERIES_LIST[s_key]['name']}**", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("bonus_"):
        s_key = query.data.split('_')[-1]
        bonus = db.get_user_bonus(user_id)
        if bonus > 0:
            series = SERIES_LIST[s_key]
            # 6వ ఎపిసోడ్ ని బోనస్ గా ఇస్తున్నాం (free_ids లో లేనిది)
            bonus_msg_id = series['free_ids'][-1] + 1 
            try:
                await context.bot.copy_message(chat_id=user_id, from_chat_id=series['cid'], message_id=bonus_msg_id)
                db.use_bonus(user_id)
                await query.message.reply_text("🎁 బోనస్ ఎపిసోడ్ పంపాను! మీ ఖాతాలో ఒక బోనస్ తగ్గించబడింది.")
            except: await query.message.reply_text("క్షమించండి, బోనస్ ఎపిసోడ్ పంపడం కుదరలేదు.")
        else:
            await query.message.reply_text("మీ దగ్గర బోనస్ ఎపిసోడ్లు లేవు. ఫ్రెండ్స్ ని రిఫర్ చేయండి!")

    elif query.data == "my_ref":
        bot_user = (await context.bot.get_me()).username
        ref_link = f"https://t.me/{bot_user}?start={user_id}"
        await query.message.reply_text(f"మీ రిఫరల్ లింక్: `{ref_link}`\n\nదీనిని మీ ఫ్రెండ్స్ కి పంపండి. వారు జాయిన్ అయితే మీ ఇద్దరికీ ఒక్కో ఎపిసోడ్ ఫ్రీగా వస్తుంది!", parse_mode='Markdown')

    elif query.data.startswith("free_"):
        s_key = query.data.split('_')[-1]
        for msg_id in SERIES_LIST[s_key]['free_ids']:
            try: await context.bot.copy_message(chat_id=user_id, from_chat_id=SERIES_LIST[s_key]['cid'], message_id=msg_id)
            except: pass

    elif query.data == "back_to_list":
        keyboard = [[InlineKeyboardButton(f"🎬 {data['name']}", callback_data=f"select_{key}")] for key, data in SERIES_LIST.items()]
        keyboard.append([InlineKeyboardButton("🔗 నా రిఫరల్ లింక్", callback_data="my_ref")])
        await query.edit_message_text("సిరీస్ జాబితా:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # (పాత స్క్రీన్‌షాట్ హ్యాండ్లింగ్ కోడ్ ఇక్కడ ఉంటుంది)
    pass

def main():
    Thread(target=run_web).start()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    application.run_polling()

if __name__ == '__main__':
    main()
