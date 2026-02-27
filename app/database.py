from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URL, MONGO_DB_NAME

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[MONGO_DB_NAME]

users_col = db["users"]
videos_col = db["videos"]
ad_sessions_col = db["ad_sessions"]
