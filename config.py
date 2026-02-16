import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL") # MongoDB Connection String
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

# ఆడియో సిరీస్ వివరాలు
SERIES_LIST = {
    "series_1": {
        "name": "మహాభారతం", 
        "price": "99", 
        "cid": -100123456789,
        "free_ids": [10, 11, 12, 13, 14] 
    },
    "series_2": {
        "name": "రామాయణం", 
        "price": "149", 
        "cid": -100987654321,
        "free_ids": [20, 21, 22, 23, 24]
    }
}
