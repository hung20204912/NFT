import requests
from pymongo import MongoClient
import time
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mongo_utils import get_mongo_collection


collection = get_mongo_collection()


headers = {"x-api-key": "2mqHS1v0NcuNo1BHYAGKM5HPK63"}


nft_collections = collection.find({})

for nft in nft_collections:
    total_owners = 0  
    
    if "contracts" in nft:
        contracts = nft["contracts"].get("0x1", []) if isinstance(nft["contracts"], dict) else []
        
        if not contracts:
            print(f"No contracts found for NFT ID: {nft['_id']}. Skipping...")
            continue
        
        for contract_address in contracts:
            if isinstance(contract_address, str) and contract_address:
                url = "https://api.chainbase.online/v1/nft/owners"
                querystring = {"chain_id": "1", "limit": "1", "contract_address": contract_address}

                response = requests.get(url, headers=headers, params=querystring)
                
                
                if response.status_code == 200:
                    data = response.json()
                    if data["code"] == 0 and "count" in data:
                        total_owners += data["count"]
                    else:
                        print(f"Error fetching data for contract {contract_address}: {data}")
                else:
                    print(f"Failed to fetch data for contract {contract_address}: {response.status_code}")

                time.sleep(1)  

    
    collection.update_one(
        {"_id": nft["_id"]},
        {"$set": {"numberOfOwners": total_owners}},
        upsert=False
    )
    print(f"Updated document with _id: {nft['_id']} - Total Owners: {total_owners}.")

print("All updates completed.")
