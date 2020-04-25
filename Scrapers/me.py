import requests
from bs4 import BeautifulSoup
import csv
import datetime

url = 'https://www.maine.gov/governor/mills/official_documents'
source = requests.get(url).text
bs = BeautifulSoup(source, 'html.parser')

emergency_orders_section = bs.find('div', class_='layout__region layout__region--content')
emergency_orders = emergency_orders_section.find_all('li')

field_names = ['Date', 'Description', 'Order_PDF_Link', 'Press_Release_Link', 'Guidance_Link']
scraped_orders = list()

# Loop through the emergency orders and extract the attributes
for emergency_order in emergency_orders:
    scraped_order = dict()

    # Get the description
    description = emergency_order.find_all('a')[0].text
    description = ' '.join(description.split('(')[0].split()[3:])
    scraped_order['Description'] = description

    date_section = emergency_order.find_all('a')[0]
    
    # Get the PDF link
    link = date_section['href']
    scraped_order['Order_PDF_Link'] = 'https://www.maine.gov' + link
    
    print(description)
    print(link)
    # Get the date
    try:
        date = emergency_order.contents[-1].split()[-1]
        if date < '3/18/2020':
            break
        else:
            scraped_order['Date'] = date
        print(date)
            
    except TypeError:
        continue    

    # Only save order if it contains the desired fields
    if len(scraped_order) >= len(field_names) - 2:
        scraped_orders.append(scraped_order)

# Create csv file for the scraped data
with open('../Outputs/me.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(scraped_orders)
