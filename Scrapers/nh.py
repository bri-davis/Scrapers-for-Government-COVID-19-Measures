import requests
from bs4 import BeautifulSoup
import csv
import datetime

url = 'https://www.governor.nh.gov/news-media/emergency-orders/'
source = requests.get(url).text
bs = BeautifulSoup(source, 'html.parser')

emergency_orders_section = bs.find('ul', class_='media-list')
emergency_orders = emergency_orders_section.findAll('li')[1:]

field_names = ['Date', 'Description', 'PDF_Link']
scraped_orders = list()

# Loop through the emergency orders and extract the attributes
for emergency_order in reversed(emergency_orders):
    scraped_order = dict()

    # First get title and PDF link
    title_section = emergency_order.find('p', class_='media-title')
    # Make sure this is order text and not another element
    if len(title_section.contents[-2]) > 1:
        # Remove preceding colon or dash
        description = ' '.join(title_section.contents[-2].split())[1:]
        scraped_order['Description'] = description
    else:
        continue

    # Get the link
    link = title_section.find('a')['href']
    scraped_order['PDF_Link'] = 'https://www.governor.nh.gov/news-media/emergency-orders/' + link
    
    # Get the date
    date_section = emergency_order.find('p', class_='media-date')
    date_section = date_section.text.split()
    month, year = date_section[0], date_section[-2]
    date = month + year
    date_format = datetime.datetime.strptime(date, '%B%Y')
    date = date_format.strftime('%m/%Y')
    scraped_order['Date'] = date

    # Only save order if it contains the desired fields
    if len(scraped_order) == len(field_names):
        scraped_orders.append(scraped_order)

# Create csv file for the scraped data
with open('../Outputs/nh.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(scraped_orders)

