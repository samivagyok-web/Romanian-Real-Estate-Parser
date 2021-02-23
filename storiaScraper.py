import re
import csv
from typing import Pattern, Text
import requests
import time
from bs4 import BeautifulSoup

def main():
    REGION = "bihor"
    TOWN = "oradea"

    forSale(REGION, TOWN)
    forRent(REGION, TOWN)
    finish = time.time()

def dataToInt(data):
    sq = 0
    pattern = re.compile(r'\d+')
    for match in pattern.finditer(data):
        sq = match.group(0)
    return int(sq)
 
def priceToInt(cost):
    money = ""
    for digit in cost:
        if digit >= '0' and digit <= '9' or digit == ',':
            if (digit == ','):
                money = money + '.'
            else:
                money = money + digit
    return float(money)
def maxPageNum(URL, page, soup):
    numOfPages = soup.find('ul', class_="pager")
    numOfPages = numOfPages.find_all('li', class_="")
    maxPage = 0
    for found in numOfPages:
        maxPage = int(found.a.text)
    return maxPage

def forSale(REGION, TOWN):
    URL = f'https://www.storia.ro/vanzare/apartament/{REGION}/{TOWN}/?nrAdsPerPage=72&page=1'

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')
 
    maxPage = maxPageNum(URL, page, soup)
 
    with open('estatesForSale.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Number of rooms', 'Area (m2)', 'Price (€)', 'Price per m2 (€)', 'Zone', 'Link'])
 
        for page in range (1, maxPage):
            URL = f'https://www.storia.ro/vanzare/apartament/{REGION}/{TOWN}/?nrAdsPerPage=72&page={page}'
 
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'lxml')
 
            listing2 = soup.find('div', class_="listing")
            offerDetails = listing2.find_all('div', class_="offer-item-details")
            for offer in offerDetails:
                params = offer.find('ul', class_="params")
 
                rooms = offer.find('li', class_="offer-item-rooms hidden-xs")   
 
                roomNum = dataToInt(rooms.text)
                sqMeter = offer.find('li', class_="hidden-xs offer-item-area")
 
                sqMeterNum = priceToInt(sqMeter.text)

                price = offer.find('li', class_="offer-item-price")
 
                price = price.text.strip()    
 
                intPrice = priceToInt(price)
 
                pricePerSq = offer.find('li', class_="hidden-xs offer-item-price-per-m")
 
                intPriceSquare = priceToInt(pricePerSq.text)
 
                zone = offer.find('p', class_="text-nowrap")
                zone = zone.text
                zone: Text = zone.split(',')[-1].strip()               
                    
                linkk = offer.find('a')['href']
 
                csv_writer.writerow([roomNum, sqMeterNum, intPrice, intPriceSquare, zone, linkk])
    return

def forRent(REGION, TOWN):
    URL = f'https://www.storia.ro/inchiriere/apartament/{REGION}/{TOWN}/?nrAdsPerPage=72&page=1'

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')
 
    maxPage = maxPageNum(URL, page, soup)
 
    with open('estatesForRent.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Number of rooms', 'Area (m2)', 'Price/month (€)', 'Zone', 'Link'])
 
        for page in range (1, maxPage):
            URL = f'https://www.storia.ro/inchiriere/apartament/{REGION}/{TOWN}/?nrAdsPerPage=72&page={page}'
 
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'lxml')
 
            listing2 = soup.find('div', class_="listing")
            offerDetails = listing2.find_all('div', class_="offer-item-details")
            for offer in offerDetails:
                params = offer.find('ul', class_="params")
 
                rooms = offer.find('li', class_="offer-item-rooms hidden-xs")   
 
                roomNum = dataToInt(rooms.text)
                sqMeter = offer.find('li', class_="hidden-xs offer-item-area")
 
                sqMeterNum = priceToInt(sqMeter.text)

                price = offer.find('li', class_="offer-item-price")
 
                price = price.text.strip()    
 
                intPrice = priceToInt(price)
 
                zone = offer.find('p', class_="text-nowrap")
                zone = zone.text
                zone = zone.split(',')[-1].strip()
 
                linkk = offer.find('a')['href']
 
                csv_writer.writerow([roomNum, sqMeterNum, intPrice, zone, linkk])
    return    

if __name__ == "__main__":
    main()
