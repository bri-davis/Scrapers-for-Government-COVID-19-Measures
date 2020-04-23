import requests
from bs4 import BeautifulSoup
import csv

url = 'https://governor.ri.gov/newsroom/orders/'
source = requests.get(url).text
bs = BeautifulSoup(source, 'html.parser')

emergency_orders_section = bs.find('div', class_='content')
emergency_orders = emergency_orders_section.findAll('li')

field_names = ['Date', 'Description', 'PDF_Link']
scraped_orders = list()
      
# Loop through the emergency orders and extract the attributes
for emergency_order in emergency_orders:
    scraped_order = dict()

    # Get the date
    date_section = emergency_order.find('em')
    if date_section != None:
        date = date_section.text.replace(' ', '')[1:-1]
        # Last order pertaining to covid
        if date < '03/09/2020':
            break
        scraped_order['Date'] = date

    # Get PDF link
    pdf_link = 'https://governor.ri.gov' + emergency_order.find('a')['href'][5:]
    scraped_order['PDF_Link'] = pdf_link

    # Get the description
    description_section = emergency_order.text.split('–')
    # No description details supplied
    if len(description_section) == 1:
        description = ''
    else: # Description details supplied
        description = description_section[1].split('(')[0]
    scraped_order['Description'] = description

    # Only save order if it contains the desired fields
    if len(scraped_order) == len(field_names):
        scraped_orders.append(scraped_order)

# Create csv file for the scraped data
with open('../Outputs/ri.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(scraped_orders)        
