import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["Atlas_URL"])

db = client["VIA-Database"]