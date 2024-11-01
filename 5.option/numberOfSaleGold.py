from pymongo import MongoClient
import requests
import time
from collections import defaultdict
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mongo_utils import get_mongo_collection


collection = get_mongo_collection()


url_template = "https://api.covalenthq.com/v1/eth-mainnet/nft_market/{contractAddress}/sale_count/"
headers = {"Authorization": "Bearer cqt_rQMDp3yMpTbKK8Wbc4K44WCMVrkc"}


nft_collections = collection.find({})

for nft in nft_collections:
    sales_logs = defaultdict(float)  
    
    contracts = nft.get("contracts", {})
    
    
    if isinstance(contracts, dict) and "0x1" in contracts:
        addresses = contracts["0x1"]
        
        if isinstance(addresses, list) and addresses:
            address = addresses[0]  
            
            
            url = url_template.format(contractAddress=address)
            querystring = {"days": "30"}
            response = requests.get(url, headers=headers, params=querystring)
            
            
            if response.status_code == 200:
                api_data = response.json()
                
                if api_data.get("data") and api_data["data"].get("items"):
                    for item in api_data["data"]["items"]:
                        epoch_time = int(time.mktime(time.strptime(item["date"], "%Y-%m-%dT%H:%M:%SZ")))
                        sale_count = float(item["sale_count"])
                        
                        
                        sales_logs[str(epoch_time)] += sale_count
                else:
                    print(f"No items data for contract address {address}.")
            else:
                print(f"Failed to fetch data for contract address {address}: {response.status_code} {response.text}")

    
    if sales_logs:
        collection.update_one(
            {"_id": nft["_id"]},
            {"$set": {"numberOfSalesLogs": dict(sales_logs)}},
            upsert=False
        )
        print(f"Updated numberOfSalesLogs for document with _id: {nft['_id']}.")

print("All updates completed.")
