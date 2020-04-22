import requests
from bs4 import BeautifulSoup

url = 'https://portal.ct.gov/Coronavirus/Pages/Emergency-Orders-issued-by-the-Governor-and-State-Agencies'
source = requests.get(url).text
bs = BeautifulSoup(source, 'html.parser')
print(bs.prettify())
