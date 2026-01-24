from pymongo import MongoClient
import os

from dotenv import load_dotenv

from Bhojanly.settings import BASE_DIR
load_dotenv(BASE_DIR / ".env")


MONGO_URL = os.environ.get("DB_URL")
MONGO_DB_NAME = os.environ.get("DB_NAME")

if not MONGO_URL or not MONGO_DB_NAME:
    raise Exception("MongoDB environment variables not set")

# collections