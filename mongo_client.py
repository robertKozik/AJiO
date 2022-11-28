from pymongo import MongoClient

class AbstractClient(object):
    def clean_push(self):
        raise NotImplementedError('subclasses must override clean_push()!')

class Client(AbstractClient):
    def __init__(self, db, url = "mongodb://myUserAdmin:test123@localhost:27017"):
        self.client = MongoClient(url)
        self.db = self.client[db]

    def push_one_to_db(self, collection, data):
        collection = self.db[collection]
        return collection.insert_one(data).inserted_id

    def push_multiple_to_db(self, collection, data):
        collection = self.db[collection]
        return collection.insert_many(data)

    def clean_push(self, collection, data):
        selected_collection = self.db[collection]
        selected_collection.drop()
        self.push_multiple_to_db(collection=collection, data=data)


# client = Client("plants")

# client.push_one_to_db('plants', {"test": "hello", "test_two": "world"})
