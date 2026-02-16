import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, PREMIUM_CHANNEL_ID, ADMIN_ID, ADMIN_USERNAME, FREE_CHANNEL_LINK

# లాగింగ్ సెటప్
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = (
        f"నమస్కారం! 🙏\n\n"
        f"మా ఉచిత ఆడియోలను ఇక్కడ వినండి: {FREE_CHANNEL_LINK}\n\n"
        f"మొత్తం ప్రీమియం ఆడియోల కోసం ₹99 చెల్లించి జాయిన్ అవ్వండి.\n"
        f"మీ యూజర్ ఐడి: `{user_id}`\n\n"
        f"పేమెంట్ తర్వాత స్క్రీన్‌షాట్‌ను {ADMIN_USERNAME} కు పంపండి."
    )
    keyboard = [[InlineKeyboardButton("పేమెంట్ వివరాలు 💳", callback_data='pay_info')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'pay_info':
        pay_text = (
            "📌 **పేమెంట్ వివరాలు:**\n"
            "UPI ID: `yourname@upi` \n\n"
            "పేమెంట్ పూర్తయ్యాక, స్క్రీన్‌షాట్‌తో పాటు పైన ఉన్న మీ **User ID** ని అడ్మిన్‌కు పంపండి."
        )
        await query.edit_message_text(text=pay_text, parse_mode='Markdown')

async def send_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # అడ్మిన్ కాకపోతే యాక్సెస్ ఇవ్వదు
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("సరైన విధానం: /sendlink [USER_ID]")
        return

    try:
        target_user_id = int(context.args[0])
        
        # వన్-టైమ్ ఇన్వైట్ లింక్ క్రియేషన్
        invite_link = await context.bot.create_chat_invite_link(
            chat_id=PREMIUM_CHANNEL_ID,
            member_limit=1,
            name=f"Premium User {target_user_id}"
        )

        await context.bot.send_message(
            chat_id=target_user_id,
            text=f"✅ మీ పేమెంట్ కన్ఫర్మ్ అయ్యింది!\nకింద ఉన్న లింక్ ద్వారా ఛానల్‌లో జాయిన్ అవ్వండి:\n\n{invite_link.invite_link}\n\n(గమనిక: ఇది ఒకరికి మాత్రమే పనిచేస్తుంది)"
        )
        await update.message.reply_text(f"User {target_user_id} కి లింక్ పంపబడింది.")

    except Exception as e:
        await update.message.reply_text(f"ఎర్రర్: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendlink", send_link))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("బాట్ రన్ అవుతోంది...")
    app.run_polling()

if __name__ == '__main__':
    main()
