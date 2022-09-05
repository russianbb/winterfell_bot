from pymongo import MongoClient

from settings import MONGODB_HOST, MONGODB_DATABASE

mongo_client = MongoClient(host=MONGODB_HOST)
db = mongo_client[MONGODB_DATABASE]
