#!/usr/bin/env python3
"""
script that provides some stats anbout Nginx logs stored in MongoDB
"""
from pymongo import MongoClient
def main(mongo_collection):
    """read and format nginx logs"""
    print(f"{mongo_collection.count_documents({})} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_stats = [collection.count_documents({'method': method}) for method in methods]
    print("Methods:")
    for method, stat in zip(methods, method_stats):
        print(f"\tmethod {method}: {stat}")
    status_logs = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_logs} status check")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client['logs']
    collection = db['nginx']
    main(collection)
