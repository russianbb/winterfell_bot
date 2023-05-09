import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
MONGODB_HOST = os.environ.get("MONGODB_URL")
MONGODB_URL = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}"

LIST_HEADER = "\n**📝 LISTA DE COMPRAS**\n\n"
