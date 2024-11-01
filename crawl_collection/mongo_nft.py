import requests
from pymongo import MongoClient
import time
import schedule

client = MongoClient("mongodb://localhost:27017/")
db = client['NFT']
collection = db['NFT_collection']
nft_collection = db['NFTs']

def fetch_nfts_from_collection(collection_slug):
    next_cursor = None
    limit = 100  
    headers = {
        "accept": "application/json",
        "x-api-key": "3e74b6ca1bb8405c8e62269341b06a57"
    }

    while True:
        if next_cursor:
            url = f"https://api.opensea.io/api/v2/collection/{collection_slug}/nfts?limit={limit}&cursor={next_cursor}"
        else:
            url = f"https://api.opensea.io/api/v2/collection/{collection_slug}/nfts?limit={limit}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            for nft_data in data.get('nfts', []):
                nft_data["_id"] = f"{nft_data['identifier']}_{nft_data['contract']}"
                nft_data['collection_slug'] = collection_slug
                nft_data['last_updated_at'] = int(time.time())

                nft_collection.update_one(
                    {"_id": nft_data["_id"]},
                    {"$set": nft_data},
                    upsert=True
                )
                print(f"Upserted NFT: {nft_data['_id']}")

            next_cursor = data.get("next")
            print(f"Next cursor: {next_cursor}")

            if not next_cursor:
                print(f"Finished fetching NFTs for collection: {collection_slug}")
                break
        else:
            print(f"Failed to fetch NFTs: {response.status_code}")
            break

        time.sleep(0.1)

def crawl_all_collections():
    for doc in collection.find({}, {"_id": 1}):
        collection_slug = doc["_id"]
        print(f"Fetching NFTs for collection: {collection_slug}")
        fetch_nfts_from_collection(collection_slug)

schedule.every().day.at("00:00").do(crawl_all_collections)

print("Scheduler started. Waiting for the scheduled time...")

while True:
    schedule.run_pending()
    time.sleep(1)
