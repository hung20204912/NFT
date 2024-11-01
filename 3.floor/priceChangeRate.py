from pymongo import MongoClient
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mongo_utils import get_mongo_collection


collection = get_mongo_collection()


nft_collections = collection.find({})


for nft in nft_collections:
    if "floorChangeLogs" in nft and nft["floorChangeLogs"]:
        floor_change_logs = nft["floorChangeLogs"]

        
        sorted_logs = sorted(floor_change_logs.items(), key=lambda x: int(x[0]), reverse=True)

        if len(sorted_logs) >= 2:
            latest_timestamp, latest_value = sorted_logs[0]  
            second_latest_timestamp, second_latest_value = sorted_logs[1] 

            try:
                
                price_change_rate = (float(latest_value) - float(second_latest_value)) / float(second_latest_value)
                
                
                collection.update_one(
                    {"_id": nft["_id"]},  
                    {"$set": {"priceChangeRate": price_change_rate}},
                    upsert=True
                )
                print(f"Updated priceChangeRate for NFT ID: {nft['_id']} to {price_change_rate:.2%}.")
            except ZeroDivisionError:
                print(f"Cannot calculate priceChangeRate for NFT ID: {nft['_id']} due to division by zero.")
        else:
            print(f"Not enough data to calculate priceChangeRate for NFT ID: {nft['_id']}.")
    else:
        print(f"No floorChangeLogs found for NFT ID: {nft['_id']}. Skipping...")

print("Price change rate calculation completed.")
