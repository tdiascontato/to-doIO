import pymongo
from decouple import config

url = config('NAME_MONGODB')
client = pymongo.MongoClient(url)

db = client['GrowingGround']