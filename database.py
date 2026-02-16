from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client['telegram_bot_db']
users_col = db['users']

def add_user(user_id):
    # యూజర్ లేకపోతేనే యాడ్ చేస్తుంది
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id})

def get_all_users():
    users = users_col.find({}, {"user_id": 1})
    return [u['user_id'] for u in users]
