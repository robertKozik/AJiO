from data_fetcher import DataFetcher
from mongo_client import Client
from urls import urls
from sys import exit

fetcher = DataFetcher(urls, Client("inflation", "mongodb+srv://root:root@cluster0.qeao0.mongodb.net/plants?retryWrites=true&w=majority"))
fetcher.fetch_data()
fetcher.save_output_as_json('data.json')
flag = fetcher.save_output_to_db("INFLATION_2017-2021")
if not flag:
    print("Process ended unsuccessfully")
    exit()
print("Process ended successfully")
