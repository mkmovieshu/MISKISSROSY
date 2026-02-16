import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, LOG_CHANNEL_ID, ADMIN_ID, ADMIN_USERNAME, SERIES_LIST

logging.basicConfig(level=logging.INFO)
app = Flask('')

@app.route('/')
def home(): return "Multi-Series Bot is Running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_text = f"🆕 **కొత్త యూజర్:**\n👤 పేరు: {user.first_name}\n🆔 ఐడి: `{user.id}`"
    try: await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_text, parse_mode='Markdown')
    except: pass

    # సిరీస్ లిస్ట్ బటన్స్ క్రియేట్ చేయడం
    keyboard = []
    for key, data in SERIES_LIST.items():
        keyboard.append([InlineKeyboardButton(f"🎬 {data['name']} - {data['price']}", callback_data=f"info_{key}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"నమస్కారం {user.first_name}! 🙏\n\nమా వద్ద ఉన్న ఆడియో సిరీస్ లు ఇక్కడ ఉన్నాయి. మీకు కావాల్సిన దానిపై క్లిక్ చేయండి:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("info_"):
        s_key = query.data.replace("info_", "")
        series = SERIES_LIST[s_key]
        
        pay_text = (
            f"🎬 **సిరీస్ పేరు:** {series['name']}\n"
            f"💰 **ధర:** {series['price']}\n"
            f"🆔 **మీ యూజర్ ఐడి:** `{query.from_user.id}`\n\n"
            f"📌 **పేమెంట్ విధానం:**\n"
            f"UPI ID: `మీ_UPI_ID_ఇక్కడ` \n\n"
            f"పేమెంట్ చేసి స్క్రీన్ షాట్ ను {ADMIN_USERNAME} కు పంపండి. "
            f"మెసేజ్ లో 'సిరీస్: {series['name']}' అని తెలపండి."
        )
        back_button = [[InlineKeyboardButton("🔙 వెనక్కి", callback_data="back_to_list")]]
        await query.edit_message_text(pay_text, reply_markup=InlineKeyboardMarkup(back_button), parse_mode='Markdown')

    elif query.data == "back_to_list":
        keyboard = []
        for key, data in SERIES_LIST.items():
            keyboard.append([InlineKeyboardButton(f"🎬 {data['name']} - {data['price']}", callback_data=f"info_{key}")])
        await query.edit_message_text("మా వద్ద ఉన్న ఆడియో సిరీస్ లు ఇక్కడ ఉన్నాయి:", reply_markup=InlineKeyboardMarkup(keyboard))

async def send_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: `/sendlink USER_ID CHANNEL_ID`", parse_mode='Markdown')
        return
    try:
        t_id, c_id = int(context.args[0]), int(context.args[1])
        link = await context.bot.create_chat_invite_link(chat_id=c_id, member_limit=1)
        await context.bot.send_message(chat_id=t_id, text=f"✅ పేమెంట్ వెరిఫై అయ్యింది!\nమీ సిరీస్ లింక్: {link.invite_link}")
        await update.message.reply_text(f"User {t_id} కి లింక్ పంపాను.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    Thread(target=run_web).start()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendlink", send_link))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
