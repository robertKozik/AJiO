from pymongo import MongoClient

class Client:
    url = "mongodb+srv://root:root@cluster0.qeao0.mongodb.net/plants?retryWrites=true&w=majority"

    def __init__(self, db):
        self.client = MongoClient(self.url)
        self.db = self.client[db]

    def push_one_to_db(self, collection, data):
        collection = self.db[collection]
        return collection.insert_one(data).inserted_id

    def push_multiple_to_db(self, collection, data):
        collection = self.db[collection]
        return collection.insert_many(data)

    def clean_push(self, collection, data):
        print(collection)
        selected_collection = self.db[collection]
        selected_collection.drop()
        self.push_multiple_to_db(collection=collection, data=data)


# client = Client("plants")

# client.push_one_to_db('plants', {"test": "hello", "test_two": "world"})
