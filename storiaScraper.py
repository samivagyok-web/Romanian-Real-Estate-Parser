import re
import csv
import requests
from bs4 import BeautifulSoup


REGION = "bihor"
TOWN = "oradea"
OFFEREDFOR = "vanzare" # vanzare/inchiriere
URL = f'https://www.storia.ro/{OFFEREDFOR}/apartament/{REGION}/{TOWN}/?page=1'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')

numOfPages = soup.find('ul', class_="pager")
numOfPages = numOfPages.find_all('li', class_="")
maxPage = 0
for found in numOfPages:
    maxPage = int(found.a.text)


with open('estates.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Number of rooms', 'Area (m2)', 'Price (€)', 'Price per m2 (€)', 'Zone', 'Link'])

    for page in range (1, maxPage):
        URL = f'https://www.storia.ro/{OFFEREDFOR}/apartament/{REGION}/{TOWN}/?page={page}'

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'lxml')

        listing2 = soup.find('div', class_="listing")
        offerDetails = listing2.find_all('div', class_="offer-item-details")
        for offer in offerDetails:
            params = offer.find('ul', class_="params")

            rooms = offer.find('li', class_="offer-item-rooms hidden-xs")   

            sqMeter = offer.find('li', class_="hidden-xs offer-item-area")

            price = offer.find('li', class_="offer-item-price")
            price = price.text.strip()    

            pricePerSq = offer.find('li', class_="hidden-xs offer-item-price-per-m")

            zone = offer.find('p', class_="text-nowrap")
            zone = zone.text
            pattern = re.compile(r'(?<=\),\s){1}\w+([-\s{1}$](\w+|\s{1})|$)')
            matches = pattern.finditer(zone)
            for match in matches:
                zone = match.group(0)

            linkk = offer.find('a')['href']

            csv_writer.writerow([rooms.text, sqMeter.text, price, pricePerSq.text, zone, linkk])
