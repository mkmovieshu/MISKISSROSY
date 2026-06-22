from motor.motor_asyncio import AsyncIOMotorClient
from vars import MONGO_URI

mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo["adultzonebot"]

users = db["users"]
ad_sessions = db["ad_sessions"]
videos = db["videos"]
