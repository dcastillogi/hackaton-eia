from dotenv import load_dotenv
import pymongo
import os

load_dotenv()

myclient = pymongo.MongoClient(os.getenv('MONGO_URI'))
mydb = myclient["main"]

def insert_user(user):
    mycol = mydb["users"]
    mycol.insert_one(user)

def get_user(telegram_id):
    mycol = mydb["users"]
    return mycol.find_one({"telegram_id": str(telegram_id)})