from pymongo.mongo_client import MongoClient

from utils import Env

env = Env()

client = MongoClient(env.URLMONGODB)

db = client[env.DBMONGODB]