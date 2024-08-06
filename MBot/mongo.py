import sys

from config import MONGO_URL

from MBot import BOT_ID
from MBot.logging import LOGGER
from motor.motor_asyncio import AsyncIOMotorClient


DB_NAME = f"AutoPostBot_{BOT_ID}"

try:
    _mongo_async_ = AsyncIOMotorClient(MONGO_URL)
    mongodb = _mongo_async_[DB_NAME]
except:
    LOGGER.info("Failed To Connect, Please Change Your Mongo Database or Try Again After Some Time !")
    sys.exit()
