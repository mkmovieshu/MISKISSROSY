import os
import logging
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import *
import database as db

logging.basicConfig(level=logging.INFO)
app = Flask('')

@app.route('/')
def home(): return "Bot with MongoDB is Live!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id) # MongoDB లో సేవ్ చేస్తుంది
    
    log_text = f"🆕 **కొత్త యూజర్:**\n👤 పేరు: {user.first_name}\n🆔 ఐడి: `{user.id}`"
    try: await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_text, parse_mode='Markdown')
    except: pass

    keyboard = [[InlineKeyboardButton(f"🎬 {data['name']}", callback_data=f"select_{key}")] for key, data in SERIES_LIST.items()]
    await update.message.reply_text("నమస్కారం! 🙏\nఒక సిరీస్ ను ఎంచుకోండి:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    s_key = query.data.split('_')[-1]

    if query.data.startswith("select_"):
        keyboard = [
            [InlineKeyboardButton("🎧 5 ఫ్రీ ఆడియోలు", callback_data=f"free_{s_key}")],
            [InlineKeyboardButton("💎 ప్రీమియం కొనండి", callback_data=f"pay_{s_key}")],
            [InlineKeyboardButton("🔙 వెనక్కి", callback_data="back_to_list")]
        ]
        await query.edit_message_text(f"🎬 **{SERIES_LIST[s_key]['name']}**", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("free_"):
        series = SERIES_LIST[s_key]
        for msg_id in series['free_ids']:
            try: await context.bot.copy_message(chat_id=query.from_user.id, from_chat_id=series['cid'], message_id=msg_id)
            except: pass

    elif query.data.startswith("pay_"):
        series = SERIES_LIST[s_key]
        pay_text = f"💎 **{series['name']}**\nధర: ₹{series['price']}\nమీ ఐడి: `{query.from_user.id}`\n\nస్క్రీన్ షాట్ ను {ADMIN_USERNAME} కు పంపండి."
        await query.edit_message_text(pay_text, parse_mode='Markdown')

    elif query.data == "back_to_list":
        keyboard = [[InlineKeyboardButton(f"🎬 {data['name']}", callback_data=f"select_{key}")] for key, data in SERIES_LIST.items()]
        await query.edit_message_text("సిరీస్ జాబితా:", reply_markup=InlineKeyboardMarkup(keyboard))

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args: return await update.message.reply_text("మెసేజ్ టైప్ చేయండి.")
    
    msg = " ".join(context.args)
    users = db.get_all_users()
    count = 0
    for u_id in users:
        try:
            await context.bot.send_message(chat_id=u_id, text=f"📢 **Update:**\n\n{msg}")
            count += 1
            await asyncio.sleep(0.05)
        except: pass
    await update.message.reply_text(f"✅ {count} మందికి పంపాను.")

async def send_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        t_id, c_id = int(context.args[0]), int(context.args[1])
        link = await context.bot.create_chat_invite_link(chat_id=c_id, member_limit=1)
        await context.bot.send_message(chat_id=t_id, text=f"✅ మీ పేమెంట్ కన్ఫర్మ్! లింక్: {link.invite_link}")
    except: pass

def main():
    Thread(target=run_web).start()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("sendlink", send_link))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
