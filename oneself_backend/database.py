from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

# 🔥 Secure connection to MongoDB Atlas with TLS
client = MongoClient(
    MONGO_URL,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["period_tracker"]

users_collection = db["users"]
cycles_collection = db["cycles"]
symptoms_collection = db["symptoms"]
