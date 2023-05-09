from pymongo import MongoClient

from settings import MONGODB_URL, MONGODB_DATABASE

mongo_client = MongoClient(host=MONGODB_URL)
db = mongo_client[MONGODB_DATABASE]
