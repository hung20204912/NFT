import requests
from pymongo import MongoClient
from datetime import datetime, timezone
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mongo_utils import get_mongo_collection


collection = get_mongo_collection()


nft_collections = collection.find({})


headers = {
    "Authorization": "Bearer cqt_rQMDp3yMpTbKK8Wbc4K44WCMVrkc"
}


for nft in nft_collections:
    if "contracts" in nft and "0x1" in nft["contracts"] and isinstance(nft["contracts"]["0x1"], list) and nft["contracts"]["0x1"]:
        address = nft["contracts"]["0x1"][0]  
        floor_price_logs = {}

        url = f"https://api.covalenthq.com/v1/eth-mainnet/nft_market/{address}/floor_price/"
        
        try:
            response = requests.get(url, headers=headers, params={"days": "30"})
            data = response.json()

            if "data" in data and "items" in data["data"]:
                for entry in data["data"]["items"]:
                    date_str = entry.get("date")
                    floor_price_quote = entry.get("floor_price_quote")
                    
                    if floor_price_quote is not None and date_str is not None:
                        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        epoch_time = int(dt.timestamp())
                        floor_price_logs[str(epoch_time)] = float(floor_price_quote)

            else:
                print(f"No data available for contract {address} or reached the end.")
        
        except Exception as e:
            print(f"Error processing contract {address}: {e}")
            continue

        
        try:
            collection.update_one(
                {"_id": nft["_id"]},
                {"$set": {"floorChangeLogs": floor_price_logs}},
                upsert=False
            )
            print(f"Updated floor price logs for {nft['_id']}.")
        except Exception as e:
            print(f"Error updating MongoDB for {nft['_id']}: {e}")
    else:
        print(f"Skipping document {nft['_id']} due to missing or empty contracts list.")

print("Update completed.")
