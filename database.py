from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client['telegram_bot_db']
users_col = db['users']

def add_user(user_id, referred_by=None):
    user = users_col.find_one({"user_id": user_id})
    if not user:
        new_user = {
            "user_id": user_id,
            "referred_by": referred_by,
            "bonus_episodes": 1 if referred_by else 0, # రిఫరల్ ద్వారా వస్తే 1 బోనస్
            "referral_count": 0
        }
        users_col.insert_one(new_user)
        # ఎవరైతే రిఫర్ చేశారో వారికి కూడా ఒక బోనస్ ఇవ్వడం
        if referred_by:
            users_col.update_one({"user_id": referred_by}, {"$inc": {"bonus_episodes": 1, "referral_count": 1}})
        return True
    return False

def get_user_bonus(user_id):
    user = users_col.find_one({"user_id": user_id})
    return user.get("bonus_episodes", 0) if user else 0

def use_bonus(user_id):
    users_col.update_one({"user_id": user_id}, {"$inc": {"bonus_episodes": -1}})

def get_all_users():
    return [u['user_id'] for u in users_col.find({}, {"user_id": 1})]
