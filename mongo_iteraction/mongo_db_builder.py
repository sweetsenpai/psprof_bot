import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

psprof_db = mongo_client["psprof"]
# Name, Contacts, Specialization, Addres
print(psprof_db.list_collection_names())