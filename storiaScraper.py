import re
import csv
import requests
from bs4 import BeautifulSoup

def dataToInt(data):
    sq = 0
    pattern = re.compile(r'\d+')
    for match in pattern.finditer(data):
        sq = match.group(0)
    return int(sq)

def priceToInt(cost):
    money = ""
    for digit in cost:
        if digit >= '0' and digit <= '9':
            money = money + digit
    return int(money)

def main():
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

                roomNum = dataToInt(rooms.text)
                sqMeter = offer.find('li', class_="hidden-xs offer-item-area")

                sqMeterNum = dataToInt(sqMeter.text)

                price = offer.find('li', class_="offer-item-price")

                price = price.text.strip()    

                intPrice = priceToInt(price)

                pricePerSq = offer.find('li', class_="hidden-xs offer-item-price-per-m")

                intPriceSquare = priceToInt(pricePerSq.text)

                zone = offer.find('p', class_="text-nowrap")
                zone = zone.text
                pattern = re.compile(r'(?<=\),\s){1}\w+([-\s{1}$](\w+|\s{1})|$)')
                matches = pattern.finditer(zone)

                for match in matches:
                    zone = match.group(0)

                linkk = offer.find('a')['href']

                csv_writer.writerow([roomNum, sqMeterNum, intPrice, intPriceSquare, zone, linkk])
 
if __name__ == "__main__":
    main()
