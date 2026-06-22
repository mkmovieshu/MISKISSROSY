from bot import bot
from pyrogram import idle
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, *args):
        pass

def run_server():
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

async def start():
    await bot.start()

bot.loop.create_task(start())
idle()
