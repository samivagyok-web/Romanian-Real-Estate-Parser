import re
import requests
from bs4 import BeautifulSoup

URL = 'https://www.storia.ro/vanzare/apartament/bihor/oradea/'
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

    print(f"{rooms.text} -- {sqMeter.text} -- {price} -- {pricePerSq.text} -- {zone} -- {linkk}")
