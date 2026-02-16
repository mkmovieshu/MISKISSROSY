import os

# Render Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

# సిరీస్ వివరాలు (పేరు, ధర, ఛానల్ ఐడి)
SERIES_LIST = {
    "series_1": {"name": "మహాభారతం ఆడియో", "price": "₹99", "cid": "-100123456789"},
    "series_2": {"name": "రామాయణం ఆడియో", "price": "₹149", "cid": "-100987654321"},
    "series_3": {"name": "కథల సిరీస్", "price": "₹49", "cid": "-100456123789"}
}
