# EBay scraper

import requests


x = requests.get('https://w3schools.com/python/demopage.htm')
x = requests.get("https://automatetheboringstuff.com/")

print(x.text)
print("kurwa")