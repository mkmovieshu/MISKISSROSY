import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, PREMIUM_CHANNEL_ID, LOG_CHANNEL_ID, ADMIN_ID, ADMIN_USERNAME, FREE_CHANNEL_LINK

# లాగింగ్ సెటప్
logging.basicConfig(level=logging.INFO)

# Render కోసం చిన్న వెబ్ సర్వర్ (Free Tier నిద్రపోకుండా ఉండటానికి)
app = Flask('')

@app.route('/')
def home():
    return "బాట్ సురక్షితంగా రన్ అవుతోంది!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# యూజర్ /start నొక్కినప్పుడు
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "No Username"
    
    # 1. లాగ్ ఛానల్‌కు వివరాలు పంపడం
    log_text = (
        "🆕 **కొత్త యూజర్ రిజిస్టర్ అయ్యారు!**\n\n"
        f"👤 పేరు: {user.first_name}\n"
        f"🆔 ఐడి: `{user_id}`\n"
        f"🔗 యూజర్ నేమ్: {username}"
    )
    try:
        await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Log Error: {e}")

    # 2. యూజర్‌కి మెసేజ్
    welcome_text = (
        f"నమస్కారం {user.first_name}! 🙏\n\n"
        f"మా ఉచిత ఆడియోల కోసం: {FREE_CHANNEL_LINK}\n\n"
        f"మొత్తం ప్రీమియం ఆడియోల కోసం ₹99 చెల్లించండి.\n"
        f"మీ యూజర్ ఐడి: `{user_id}`\n\n"
        f"స్క్రీన్‌షాట్‌ను {ADMIN_USERNAME} కు పంపండి."
    )
    keyboard = [[InlineKeyboardButton("పేమెంట్ వివరాలు 💳", callback_data='pay_info')]]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# బటన్ క్లిక్ చేసినప్పుడు
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'pay_info':
        await query.edit_message_text(
            "📌 **పేమెంట్ వివరాలు:**\n\n"
            "UPI ID: `మీ_యూపీఐ_ఐడి_ఇక్కడ` \n\n"
            "పేమెంట్ పూర్తయ్యాక, స్క్రీన్‌షాట్‌తో పాటు మీ User ID ని అడ్మిన్‌కు పంపండి.",
            parse_mode='Markdown'
        )

# అడ్మిన్ లింక్ పంపడానికి (/sendlink 12345)
async def send_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("సరైన విధానం: /sendlink [USER_ID]")
        return
    try:
        target_id = int(context.args[0])
        link = await context.bot.create_chat_invite_link(chat_id=PREMIUM_CHANNEL_ID, member_limit=1)
        await context.bot.send_message(chat_id=target_id, text=f"✅ పేమెంట్ వెరిఫై అయ్యింది! లింక్: {link.invite_link}")
        await update.message.reply_text(f"User {target_id} కి లింక్ పంపాను.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    # వెబ్ సర్వర్ స్టార్ట్
    Thread(target=run_web).start()
    
    # బాట్ స్టార్ట్
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendlink", send_link))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("బాట్ స్టార్ట్ అయ్యింది...")
    application.run_polling()

if __name__ == '__main__':
    main()
    
