import requests
from bs4 import BeautifulSoup
import csv
import datetime
import re

# Retrieve source text
url = 'https://portal.ct.gov/Coronavirus/Pages/Emergency-Orders-issued-by-the-Governor-and-State-Agencies'
source = requests.get(url).text
bs = BeautifulSoup(source, 'html.parser')

# Portion of page containing orders
emergency_orders_section = bs.find('tbody')
emergency_orders = emergency_orders_section.findAll('td')

# Elements being scraped
field_names = ['Date', 'Description', 'Order_PDF_Link']
scraped_orders = list()

# Loop through the emergency orders and extract the attributes
for emergency_order in emergency_orders:
    scraped_order = dict()

    # First get date and PDF link
    title_section = emergency_order.find('p')
    # Make sure it's an order, otherwise skip it
    if title_section != None:
        # Break off unrelated text
        date = title_section.text.split(':')[0]
        # Change date format
        date_format = datetime.datetime.strptime(date, '%B %d, %Y')
        date = date_format.strftime('%m/%d/%Y')
        scraped_order['Date'] = date
        
        # Get the PDF link
        pdf_link = 'https://portal.ct.gov' + title_section.find('a')['href']
        scraped_order['PDF_Link'] = pdf_link

    # Get the description
    text_section = emergency_order.findAll('li')
    # Make sure it's an order, otherwise skip it
    if text_section != None:
        lines = list()
        # Combine the various sentences into one string.
        for line in text_section:
            lines.append(' ' + line.text + '.')
        description = ''.join(lines)
        # Remove excess whitespace
        _RE_COMBINE_WHITESPACE = re.compile(r'\s+')
        description = _RE_COMBINE_WHITESPACE.sub(' ', description).strip()
        scraped_order['Description'] = description

    # Only save order if it contains the desired fields
    if len(scraped_order) == len(field_names):
        scraped_orders.append(scraped_order)

# Create csv file for the scraped data
with open('../Outputs/ct.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(scraped_orders)
        
        
