from pymongo import MongoClient
from datetime import datetime
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mongo_utils import get_mongo_collection


collection = get_mongo_collection()


chain_mapping = {
    "ethereum": "0x1",
    "polygon": "0x89",
    "binance-smart-chain": "0x38"
}
eth_price = 2533.41


for nft in collection.find({}):
    updates = {}
    unset_fields = {}
    needs_update = False  

    
    if "total_supply" in nft:
        updates["totalSupply"] = nft["total_supply"]
        updates["numberOfItems"] = nft["total_supply"]
        unset_fields["total_supply"] = "" 

    if "last_updated_at" in nft:
        updates["lastUpdatedAt"] = nft["last_updated_at"]
        unset_fields["last_updated_at"] = "" 

    if "banner_image_url" in nft:
        updates["bannerUrl"] = nft["banner_image_url"]
        unset_fields["banner_image_url"] = "" 

    if "image_url" in nft:
        updates["imageUrl"] = nft["image_url"]
        unset_fields["image_url"] = "" 

    if "collection_offers_enabled" in nft:
        updates["collectionOffersEnabled"] = nft["collection_offers_enabled"]
        unset_fields["collection_offers_enabled"] = ""     

    if "is_disabled" in nft:
        updates["isDisabled"] = nft["is_disabled"]
        unset_fields["is_disabled"] = ""    

    if "is_nsfw" in nft:
        updates["isNsfw"] = nft["is_nsfw"]
        unset_fields["is_nsfw"] = ""    

    if "safelist_status" in nft:
        updates["safelistStatus"] = nft["safelist_status"]
        unset_fields["safelist_status"] = ""   

    if "trait_offers_enabled" in nft:
        updates["traitOffersEnabled"] = nft["trait_offers_enabled"]
        unset_fields["trait_offers_enabled"] = ""  

    if "created_date" in nft:
        updates["createdDate"] = nft["created_date"]
        unset_fields["created_date"] = ""  

    if "sources" not in nft:
        updates["sources"] = ["nft"]

    
    if "floorChangeLogs" in nft and nft["floorChangeLogs"]:
        latest_floor_log = max(nft["floorChangeLogs"].items(), key=lambda x: int(x[0]))
        updates["price"] = float(latest_floor_log[1]) * eth_price

    
    if "volumeChangeLogs" in nft and nft["volumeChangeLogs"]:
        latest_volume_log = max(nft["volumeChangeLogs"].items(), key=lambda x: int(x[0]))
        updates["volume"] = float(latest_volume_log[1])

    updates["idOpensea"] = nft["_id"]

    
    if "payment_tokens" in nft:
        updated_tokens = []
        for token in nft['payment_tokens']:
            updated_token = token.copy()

            if "eth_price" in updated_token:
                updated_token["ethPrice"] = updated_token.pop("eth_price")
                needs_update = True
            if "usd_price" in updated_token:
                updated_token["usdPrice"] = updated_token.pop("usd_price")
                needs_update = True

            updated_tokens.append(updated_token)

        if needs_update:
            updates["paymentTokens"] = updated_tokens
            unset_fields["payment_tokens"] = ""  

    
    links = {}
    if "opensea_url" in nft:
        links["opensea"] = nft["opensea_url"]
    if "twitter_username" in nft:
        links["twitter"] = f"https://www.twitter.com/{nft['twitter_username']}"
    if "instagram_username" in nft:
        links["instagram"] = f"https://instagram.com/{nft['instagram_username']}"
    if "telegram_url" in nft:
        links["telegram"] = nft["telegram_url"]
    if "wiki_url" in nft:
        links["wiki"] = nft["wiki_url"]
    if "discord_url" in nft:
        links["discord"] = nft["discord_url"]
    if "project_url" in nft:
        links["website"] = nft["project_url"]

    if links:
        updates["links"] = links

    
    unset_fields.update({
        "opensea_url": "",
        "twitter_username": "",
        "instagram_username": "",
        "telegram_url": "",
        "wiki_url": "",
        "discord_url": "",
        "project_url": ""
    })

    
    if updates:
        update_query = {"$set": updates}
        if unset_fields:
            update_query["$unset"] = unset_fields

        collection.update_one(
            {"_id": nft["_id"]},
            update_query,
            upsert=False
        )
        print(f"Updated document with _id: {nft['_id']}.")

print("All updates completed.")
