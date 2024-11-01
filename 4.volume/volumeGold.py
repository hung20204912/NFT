import requests
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mongo_utils import get_mongo_collection


collection = get_mongo_collection()


nft_collections = collection.find({})

headers = {"Authorization": "Bearer cqt_rQMDp3yMpTbKK8Wbc4K44WCMVrkc"}
eth_price = 2533.41  

for nft in nft_collections:
    
    if "contracts" in nft and nft["contracts"]:
        contract_addresses = nft["contracts"].get("0x1", []) if isinstance(nft["contracts"], dict) else []
        
        if not contract_addresses:
            print(f"No contract addresses found for NFT ID: {nft['_id']}. Skipping...")
            continue
        
        for contract_address in contract_addresses:
            url = f"https://api.covalenthq.com/v1/eth-mainnet/nft_market/{contract_address}/volume/"
            querystring = {"days": "30"}
            
            try:
                response = requests.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                else:
                    print(f"Skipping contract {contract_address} due to non-200 response: {response.status_code}")
                    continue  
                
                if data is not None and "data" in data and "items" in data["data"]:
                    volume_change_logs = {}

                    for item in data["data"]["items"]:
                        date_str = item.get("date")
                        volume_quote = item.get("volume_quote")
                        volume_native_quote = item.get("volume_native_quote")

                        if date_str is None:
                            print(f"Skipping entry with NoneType date for contract {contract_address}.")
                            continue

                        
                        epoch_time = int((datetime.fromisoformat(date_str[:-1]).replace(tzinfo=timezone.utc) - timedelta(hours=7)).timestamp())

                        
                        if volume_quote is None or volume_quote == 0:
                            if volume_native_quote is not None:
                                volume_quote = volume_native_quote * eth_price
                            else:
                                print(f"Skipping entry due to missing volume data for contract {contract_address}.")
                                continue  

                        volume_change_logs[str(epoch_time)] = float(volume_quote)

                    
                    collection.update_one(
                        {"_id": nft["_id"]},  
                        {"$set": {"volumeChangeLogs": volume_change_logs}},
                        upsert=True
                    )

                    print(f"Updated volumeChangeLogs for contract {contract_address}.")
                else:
                    print(f"Skipping contract {contract_address} due to missing or invalid data.")

            except Exception as e:
                print(f"Error processing contract {contract_address}: {e}")
                continue  

print("Update completed.")
