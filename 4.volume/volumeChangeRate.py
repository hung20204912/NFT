from pymongo import MongoClient
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mongo_utils import get_mongo_collection


collection = get_mongo_collection()


nft_collections = collection.find({})


for nft in nft_collections:
    volume_logs = nft.get("volumeChangeLogs")
    
    if volume_logs and len(volume_logs) >= 2:
        
        sorted_logs = sorted(volume_logs.items(), key=lambda x: int(x[0]), reverse=True)
        last_timestamp, last_value = sorted_logs[0]
        second_last_timestamp, second_last_value = sorted_logs[1]
        
        
        volume_change_rate = (last_value - second_last_value) / second_last_value if second_last_value != 0 else None
        
        
        collection.update_one(
            {"_id": nft["_id"]},
            {"$set": {"volumeChangeRate": volume_change_rate}},
            upsert=False
        )
        
        print(f"Updated document with _id: {nft['_id']} - Volume Change Rate: {volume_change_rate:.2%}" if volume_change_rate is not None else f"Volume Change Rate for {nft['_id']} is undefined (second last value is 0).")

print("All updates completed.")
