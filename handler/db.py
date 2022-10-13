import pymongo
import os

__all__ = ['client', 'db', 'col_users', 'col_guilds']

client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client["snapchat-bot"]
col_guilds = db["servers"]
col_users = db["servers"]

