'''
Ebay Scraper Request Logic
'''
import requests
from config import HEADERS

class EbayScraper():
    def __init__(self):
        self.base_url = "https://www.ebay.co.uk/sch/i.html"
        self.headers = HEADERS
    
    def search(self, keywords):
        search_url = f"{self.base_url}?_nkw={keywords}"
        return requests.get(search_url, headers=self.headers)

   