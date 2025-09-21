'''
Ebay Scraper Request Logic (Async)
'''
import aiohttp
from monitor.config import HEADERS

class EbayScraper():
    def __init__(self):
        self.base_url = "https://www.ebay.co.uk/sch/i.html"
        self.headers = HEADERS
    

    async def search(self, keywords):
        search_url = f"{self.base_url}?_nkw={keywords}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(search_url) as response:
                html = await response.text()
                return html, response.status
    
    def get_listing_url(self, listing_element):
        """Extract the URL from a listing element"""
        try:
            link_element = listing_element.find('a', href=True)
            if link_element:
                href = link_element.get('href')
                if href.startswith('/'):
                    return f"https://www.ebay.co.uk{href}"
                elif href.startswith('http'):
                    return href
        except:
            pass
        return None

   