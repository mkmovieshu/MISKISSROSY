import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, LOG_CHANNEL_ID, ADMIN_ID, ADMIN_USERNAME, FREE_CHANNEL_LINK

# లాగింగ్
logging.basicConfig(level=logging.INFO)

# Render కోసం వెబ్ సర్వర్
app = Flask('')

@app.route('/')
def home():
    return "మల్టిపుల్ సిరీస్ బాట్ రన్ అవుతోంది!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# /start కమాండ్
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # లాగ్ ఛానల్‌కు వివరాలు
    log_text = f"🆕 **కొత్త యూజర్:**\n👤 పేరు: {user.first_name}\n🆔 ఐడి: `{user_id}`"
    try:
        await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_text, parse_mode='Markdown')
    except: pass

    welcome_text = (
        f"నమస్కారం {user.first_name}! 🙏\n\n"
        f"మా ఆడియో సిరీస్ ల కోసం ₹99 చెల్లించి జాయిన్ అవ్వండి.\n"
        f"మీ యూజర్ ఐడి: `{user_id}`\n\n"
        f"పేమెంట్ స్క్రీన్‌షాట్ ను {ADMIN_USERNAME} కు పంపండి."
    )
    keyboard = [[InlineKeyboardButton("పేమెంట్ వివరాలు 💳", callback_data='pay_info')]]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# బటన్ హ్యాండ్లర్
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'pay_info':
        await query.edit_message_text(
            "📌 **పేమెంట్ వివరాలు:**\n\nUPI ID: `మీ_UPI_ID` \n\n"
            "స్క్రీన్‌షాట్‌తో పాటు మీ User ID ని పంపండి.",
            parse_mode='Markdown'
        )

# అడ్మిన్ లింక్ పంపడానికి (వాడే విధానం: /sendlink [USER_ID] [CHANNEL_ID])
async def send_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("సరైన విధానం: `/sendlink USER_ID CHANNEL_ID`", parse_mode='Markdown')
        return

    try:
        target_user_id = int(context.args[0])
        target_channel_id = int(context.args[1])
        
        # నిర్దిష్ట సిరీస్ ఛానల్ కోసం వన్-టైమ్ లింక్
        link = await context.bot.create_chat_invite_link(
            chat_id=target_channel_id, 
            member_limit=1
        )

        await context.bot.send_message(
            chat_id=target_user_id, 
            text=f"✅ మీ పేమెంట్ వెరిఫై అయ్యింది!\nమీరు కోరిన సిరీస్ లింక్ ఇక్కడ ఉంది:\n\n{link.invite_link}"
        )
        await update.message.reply_text(f"User {target_user_id} కి ఛానల్ {target_channel_id} లింక్ పంపాను.")
    
    except Exception as e:
        await update.message.reply_text(f"ఎర్రర్: {e}")

def main():
    Thread(target=run_web).start()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendlink", send_link))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
    
