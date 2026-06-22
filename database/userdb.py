from motor.motor_asyncio import AsyncIOMotorClient
from vars import MONGO_URI

mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo["adultzonebot"]

users = db["users"]
ad_sessions = db["ad_sessions"]
videos = db["videos"]

class UserDB:
    def __init__(self):
        self.users = users
        self.banned_users = db["banned_users"]

    async def get_user(self, user_id: int):
        return await self.users.find_one({"user_id": user_id})

    async def addUser(self, user_id: int, name: str):
        await self.users.insert_one({"user_id": user_id, "name": name, "plan": "free", "daily_count": 0, "daily_limit": 5})

    async def get_all_users(self):
        return await self.users.find().to_list(length=None)

    async def is_user_banned(self, user_id: int):
        return await self.banned_users.find_one({"user_id": user_id}) is not None

    async def ban_user(self, user_id: int, reason=None):
        try:
            await self.banned_users.insert_one({"user_id": user_id, "reason": reason or "No reason"})
            return True
        except:
            return False

    async def unban_user(self, user_id: int):
        result = await self.banned_users.delete_one({"user_id": user_id})
        return result.deleted_count > 0

    async def delete_user(self, user_id: int):
        await self.users.delete_one({"user_id": user_id})

udb = UserDB()
