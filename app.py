from flask import Flask
from bot import bot
import asyncio
import threading
from pyrogram import idle

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'TechifyBots is Running Successfully! 🎉'

def run_bot():
    """బాట్‌ను విడిగా రన్ చేయడానికి ఒక సురక్షితమైన మార్గం"""
    try:
        # కొత్త ఈవెంట్ లూప్‌ను క్రియేట్ చేయడం
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # బాట్‌ను స్టార్ట్ చేయడం
        loop.run_until_complete(bot.start())
        print("--- బాట్ ఆన్‌లైన్‌లోకి వచ్చింది! ---")
        
        # బాట్ నిరంతరం రన్ అవ్వడానికి
        loop.run_until_complete(idle())
    except Exception as e:
        print(f"బాట్ రన్ చేయడంలో లోపం: {e}")

# ఇది చాలా ముఖ్యం: 
# Gunicorn లోడ్ అయినప్పుడు బాట్ థ్రెడ్ కేవలం ఒకేసారి స్టార్ట్ అవుతుంది.
# ఇక్కడ ఎక్కడా app.run() వాడకూడదు.
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()
