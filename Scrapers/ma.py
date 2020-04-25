import requests
from bs4 import BeautifulSoup
import csv
import datetime

# Retrieve source text
url = 'https://www.mass.gov/info-details/covid-19-state-of-emergency'
source = requests.get(url).text
bs = BeautifulSoup(source, 'html.parser')

# Portion of page containing orders
emergency_orders_section = bs.find('div', class_='page-content')
emergency_orders = emergency_orders_section.findAll('p')

# Elements being scraped
field_names = ['Date', 'Description', 'Order_PDF_Link', 'Press_Release_Link', 'Guidance_Link']
scraped_orders = list()

# Loop through the emergency orders and extract the attributes
for emergency_order in emergency_orders:
    scraped_order = dict()

    # Get the description
    text_section = emergency_order.text
    # Alleviate inconsistent use of colons and periods, then split by period for summary
    description = text_section.replace(':', '.').split('.')[1]
    scraped_order['Description'] = description

    # Get the date
    date = ' '.join(description.split()[1:3])[:-1]
    # Change date format
    try:
        date_format = datetime.datetime.strptime(date, '%B %d')
        date = date_format.strftime('%m/%d/2020')
        scraped_order['Date'] = date
    # Discard elements of page that are not orders
    except ValueError:
        continue

    # Get the links
    link_section = emergency_order.findAll('a')
    for link in link_section:
        # Use text from link section to decipher which type of link it is
        if 'ORDER' in link.text:
            scraped_order['Order_PDF_Link'] = 'https://www.mass.gov' + link['href']
        elif 'GUIDANCE' in link.text:
            scraped_order['Guidance_Link'] = 'https://www.mass.gov' + link['href']
        elif 'PRESS' in link.text:
            scraped_order['Press_Release_Link'] = 'https://www.mass.gov' + link['href']
        else:
            continue
            
    # Only save order if it contains the desired fields
    if len(scraped_order) >= len(field_names) - 2:
        scraped_orders.append(scraped_order)

# Scrape the initial state of emergency declaration
scraped_order = dict()
initial_order = bs.find('div', class_='pre-content').find('p')
description = initial_order.text.replace(':', '.')
scraped_order['Description'] = description
date = ' '.join(description.split()[1:3])[:-1]
date_format = datetime.datetime.strptime(date, '%B %d')
date = date_format.strftime('%m/%d/2020')
scraped_order['Date'] = date
order_link = 'https://www.mass.gov' + initial_order.find('a')['href']
scraped_order['Order_PDF_Link'] = order_link
scraped_orders.append(scraped_order)

# Create csv file for the scraped data
with open('Outputs/ma.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(scraped_orders)
        
