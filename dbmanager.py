from pymongo import MongoClient
import os 
from dotenv import load_dotenv

class DatabaseManager:
    def __init__(self, mongodb_uri):
        self.client = MongoClient(mongodb_uri)

        self.db = self.client['lastprice']
        self.collection = self.db["price_info"]

    def count_price_info_mongoDB(self):

        count = self.collection.count_documents({})
        return count
        
    def extract_price_info_mongoDB(self):
        info_dict = self.collection.find().sort('_id', -1).limit(1)
        return info_dict.next()
            
    def insert_price_info_mongoDB(self, info_dict):

        self.collection.insert_one(info_dict)
        
        