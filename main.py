from data_fetcher import DataFetcher
from mongo_client import Client
from urls import urls
from sys import exit

fetcher = DataFetcher(urls, Client("plants"))
fetcher.fetch_data()
fetcher.save_output_as_json('data.json')
flag = fetcher.save_output_to_db("testCollection")
if not flag:
    print("Process ended unsuccessfully")
    exit()
print("Process ended successfully")
