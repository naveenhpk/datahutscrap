import requests
from bs4 import BeautifulSoup

baseurl = "https://carbon38.com/collections"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = 'https://carbon38.com/en-in/collections/tops?filter.p.m.custom.available_or_waitlist=1'
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.content, 'lxml')

productlist = soup.find_all('div', class_='ProductItem__Wrapper')

productlink = []
for item in productlist:
    link = item.find('a', href=True)
    if link and 'href' in link.attrs:
        productlink.append(link['href'])

# Print the extracted product links
for link in productlink:
    print(link)
