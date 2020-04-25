import requests
from bs4 import BeautifulSoup
import csv
import datetime

url = 'https://governor.vermont.gov/covid19response'
source = requests.get(url).text
bs = BeautifulSoup(source, 'html.parser')

emergency_orders_section = bs.find_all('div', class_='field-item even')
emergency_orders = emergency_orders_section[1].find_all('li')

field_names = ['Date', 'Description', 'Order_PDF_Link', 'Press_Release_Link', 'Guidance_Link']
scraped_orders = list()

# Loop through the emergency orders and extract the attributes
for emergency_order in emergency_orders:
    scraped_order = dict()

    # Get the description
    text_section = emergency_order.text
    # Remove the order type and delete excess spaces
    description = text_section.split('|')[0]
    description = ' '.join(description.split()[:-2])
    scraped_order['Description'] = description

    # Get the date
    date = ' '.join(description.split()[1:3])
    # Change date format
    try:
        date_format = datetime.datetime.strptime(date, '%B %d,')
        date = date_format.strftime('%m/%d/2020')
        scraped_order['Date'] = date
    # Data from incorrect sections will be passed over
    except ValueError:
        continue

    # Get the links
    link_section = emergency_order.findAll('a')
    for link in link_section:
        if 'Addendum' in link.text or 'Directive' in link.text:
            # Use the direct PDF link
            if 'pdf' in link['href']:
                scraped_order['Order_PDF_Link'] = link['href']
            # Access PDF on link['href']
            else: 
                source = requests.get(link['href']).text
                bs = BeautifulSoup(source, 'html.parser')
                pdf_link = bs.find('span', class_='file').find('a')['href']
                scraped_order['Order_PDF_Link'] = pdf_link
        elif 'Guidance' in link.text:
            scraped_order['Guidance_Link'] = link['href']
        elif 'Press Release' in link.text:
            scraped_order['Press_Release_Link'] = link['href']
        else:
            continue

    # Only save order if it contains the desired fields
    if len(scraped_order) >= len(field_names) - 2:
        scraped_orders.append(scraped_order)

# Create csv file for the scraped data
with open('../Outputs/vt.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(scraped_orders)

