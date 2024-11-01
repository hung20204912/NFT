from pymongo import MongoClient


def read_mongo_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

def get_mongo_collection(config_file='config.txt'):
    config = read_mongo_config(config_file)
    client = MongoClient(config['mongo_uri'])
    db = client[config['db_name']]
    collection = db[config['collection_name']]
    return collection
