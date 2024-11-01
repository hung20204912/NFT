from pymongo import MongoClient
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mongo_utils import get_mongo_collection


collection = get_mongo_collection()


nft_collections = collection.find({})


for rank, nft in enumerate(nft_collections, start=1):
    collection.update_one(
        {"_id": nft["_id"]},  
        {"$set": {"rank": rank}},  
        upsert=True  
    )
    print(f"Updated rank for NFT ID: {nft['_id']} to {rank}.")

print("Rank update completed.")
