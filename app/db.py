from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()



MONGO_DB_URL = os.environ.get("MONGO_DB_URL")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
client = AsyncIOMotorClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]  