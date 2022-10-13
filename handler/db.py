import pymongo

__all__ = ['client', 'db', 'col']

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["snapchat-bot"]
col = db["servers"]

