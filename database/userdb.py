from motor.motor_asyncio import AsyncIOMotorClient
from vars import MONGO_URL, MONGO_DB_NAME

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[MONGO_DB_NAME]

users = db["users"]
ad_sessions = db["ad_sessions"]
videos = db["videos"]
