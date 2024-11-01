from pymongo import MongoClient
import sys
import os
import logging


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongo_utils import get_mongo_collection, read_mongo_config


logging.basicConfig(level=logging.INFO, filename='transform_contracts.log')


collection = get_mongo_collection()

def transform_contracts():
    try:
        documents = collection.find()

        for doc in documents:
            if 'contracts' in doc and isinstance(doc['contracts'], list):
                addresses = [contract['address'] for contract in doc['contracts'] if contract.get('chain') == 'ethereum']

                if addresses:
                    transformed_contracts = {
                        "0x1": addresses
                    }

                    collection.update_one(
                        {"_id": doc["_id"]},
                        {"$set": {"contracts": transformed_contracts}}
                    )
                    logging.info(f"Updated document ID: {doc['_id']} with transformed contracts")
                else:
                    logging.info(f"Skipped document ID: {doc['_id']} (no Ethereum contracts found)")
            else:
                logging.info(f"Skipped document ID: {doc['_id']} (invalid contracts structure)")
    except Exception as e:
        logging.error(f"An error occurred while transforming contracts: {e}")


transform_contracts()
