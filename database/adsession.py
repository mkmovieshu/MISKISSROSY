"""
Ad Watch Token System - User చూసిన ad కి reward ఇస్తుంది
"""
from motor.motor_asyncio import AsyncIOMotorClient
from vars import MONGO_URI
from datetime import datetime, timedelta
import secrets

class AdSessionDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client["adultzonebot"]
        self.sessions = self.db["ad_sessions"]

    async def create_session(self, user_id: int, reward_videos: int = 5) -> dict:
        """Ad watch కోసం session create చేయి"""
        # పాత sessions delete చేయి
        await self.sessions.delete_many({"user_id": user_id, "watched": False})
        
        token = secrets.token_hex(16)
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        session = {
            "user_id": user_id,
            "token": token,
            "reward_videos": reward_videos,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "watched": False,
            "verified_at": None
        }
        
        result = await self.sessions.insert_one(session)
        return {
            "token": token,
            "link": f"https://t.me/your_bot?start=av_{token}"
        }

    async def get_session(self, user_id: int, token: str) -> dict:
        """Token details get చేయి"""
        session = await self.sessions.find_one({
            "user_id": user_id,
            "token": token,
            "watched": False
        })
        return session

    async def verify_session(self, user_id: int, token: str) -> bool:
        """Ad watched చేసిన చెక్ చేయి"""
        session = await self.get_session(user_id, token)
        
        if not session:
            return False
        
        # Expired చెక్
        if datetime.utcnow() > session["expires_at"]:
            await self.sessions.delete_one({"_id": session["_id"]})
            return False
        
        # Mark as watched
        await self.sessions.update_one(
            {"_id": session["_id"]},
            {
                "$set": {
                    "watched": True,
                    "verified_at": datetime.utcnow()
                }
            }
        )
        
        return True

    async def get_reward(self, user_id: int, token: str) -> int:
        """Ad చూసిన user కి reward videos return చేయి"""
        session = await self.sessions.find_one({
            "user_id": user_id,
            "token": token,
            "watched": True
        })
        
        if session:
            return session.get("reward_videos", 5)
        return 0

    async def clean_expired_sessions(self):
        """Expired sessions delete చేయి"""
        result = await self.sessions.delete_many({
            "expires_at": {"$lt": datetime.utcnow()}
        })
        return result.deleted_count

# Global instance
addb = AdSessionDB()
