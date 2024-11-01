import requests
import time
from datetime import datetime
from pymongo import MongoClient
import sys
import os
import logging


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongo_utils import get_mongo_collection, read_mongo_config


logging.basicConfig(level=logging.INFO, filename='opensea_data.log')


config = read_mongo_config('config.txt')
api_calls = int(config['api_calls'])
limit = int(config['limit'])

collection = get_mongo_collection()

def fetch_and_store_opensea_data():
    next_cursor = None  
    last_successful_cursor = None  
    max_retries = 50  

    for i in range(api_calls): 
        logging.info(f"Running API call {i + 1} at {datetime.now()}")

        retries = 0  

        while retries < max_retries:
            current_limit = limit if next_cursor is None else limit + 1  

            
            url = f"https://api.opensea.io/api/v2/collections?limit={current_limit}" + (f"&next={next_cursor}&order_by=market_cap" if next_cursor else "&order_by=market_cap")

            headers = {
                "accept": "application/json",
                "x-api-key": "3e74b6ca1bb8405c8e62269341b06a57"
            }

            try:
                
                response = requests.get(url, headers=headers)
                response.raise_for_status()  

                data = response.json()

                if 'collections' in data:
                    for collection_data in data['collections']:
                        collection_data["_id"] = collection_data["collection"]
                        collection_data['last_updated_at'] = int(datetime.now().timestamp())

                        
                        collection.update_one(
                            {"_id": collection_data["_id"]},  
                            {"$set": collection_data},  
                            upsert=True  
                        )
                        logging.info(f"Upserted collection: {collection_data['name']} at {datetime.now()}")

                        
                        url_detail = f"https://api.opensea.io/api/v2/collections/{collection_data['collection']}"
                        response_detail = requests.get(url_detail, headers=headers)

                        if response_detail.status_code == 200:
                            detail_data = response_detail.json()
                            collection.update_one(
                                {"_id": collection_data["_id"]},
                                {"$set": detail_data},
                                upsert=True
                            )
                            logging.info(f"Updated detail data for {collection_data['name']}")

                    last_successful_cursor = next_cursor 
                    next_cursor = data.get("next")  

                    if not next_cursor:
                        logging.info("No more data to fetch, stopping early.")
                        logging.info("Task completed.")
                        return  

                    time.sleep(1)  
                    break 
                else:
                    logging.warning("No collections found in response.")
                    break

            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching data from OpenSea: {e}")
                retries += 1
                if retries < max_retries:
                    logging.info(f"Retrying... ({retries}/{max_retries})")
                    time.sleep(1) 
                else:
                    logging.error("Max retries reached, using last successful cursor and retrying.")
                    next_cursor = last_successful_cursor  
                    break  

fetch_and_store_opensea_data()
