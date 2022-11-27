import requests
import helpers
import json
from bs4 import BeautifulSoup

from mongo_client import AbstractClient

class DataFetcher:

    def __init__(self, urls: list, db_client: AbstractClient):
        self.urls = urls
        self.output_dict = []
        self.db_client = db_client

    def fetch_data(self) -> None:
        for url in self.urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            output_dict = helpers.extract_table_data(soup)
            self.output_dict = output_dict
        return self.output_dict

    def save_output_as_json(self, file_name: str) -> dict:
        with open(file_name, 'w') as outfile:
            json.dump(self.output_dict, outfile)

    def save_output_to_db(self, collection_name: str) -> bool:
        try:
            self.db_client.clean_push(collection_name, self.output_dict)
            return True
        finally:
            return False

    