from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import sqlite3

def HotelScraper(destination_input):

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    opt = Options()

    opt.add_argument(r"--silent")
    opt.add_argument(r"--no-sandbox")
    opt.add_argument(r"--disable-dev-shm-usage")
    opt.add_argument(r'--ignore-certificate-errors')
    opt.add_experimental_option("detach", True)
    opt.add_argument('headless')
    opt.add_argument(f'user-agent={user_agent}')
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=opt)

    htl = 'https://www.google.com/travel/search?ved=0CAAQ5JsGahcKEwiovK3687yAAxUAAAAAHQAAAAAQBg'
    driver.get(htl)

    clear_location = '/html/body/c-wiz[2]/div/c-wiz/div[1]/div[1]/div[1]/c-wiz/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/div[3]/button'
    element = (By.XPATH, clear_location)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

    location_input = '/html/body/c-wiz[2]/div/c-wiz/div[1]/div[1]/div[1]/c-wiz/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/input'
    element = (By.XPATH, location_input)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(destination_input + '\n')

    time.sleep(4)

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    count = 0

    hotels = soup.find_all("a", class_='spNMC lRagtb')

    count = 0

    hotel_1 = {

    }

    for hotel in hotels:
        count += 1
        hotel_rating = hotel.get("aria-label")
        match = re.search(r'([\d.]+) out of [\d.]+ stars from [\d,]+ reviews, (.+)', hotel_rating)
        if match:
            rating = match.group(1)
            location = match.group(2)
            print(f"Rating: {rating}, Location: {location}")
        if count == 1:
            hotel_1 = {
                "Rating": rating,
                "Location": location
            }
        if count == 2:
            hotel_2 = {
                "Rating": rating,
                "Location": location
            }
        if count == 3:
            hotel_3 = {
                "Rating": rating,
                "Location": location
            }
            break
        
    count = 0

    prices = soup.find_all("a", class_='OxGZuc W8vlAc lRagtb')

    for price in prices:
        count += 1
        base_price = price.get("aria-label")
        match = re.search(r'Prices starting from \$([\d]+)', base_price)
        if match:
            price = match.group(1)
            print(f"Price: ${price}")
        if count == 1:
            hotel_1_price = {
                "Price": price
            }
        if count == 2:
            hotel_2_price = {
                "Price": price
            }
        if count == 3:
            hotel_3_price = {
                "Price": price
            }
            break
    count = 0

    links = soup.find_all("a", class_='PVOOXe')

    for link in links:
        count += 1
        hyperlink = link.get("href")
        if count == 1:
            hotel_1_link = {
                "Link": hyperlink
            }
        if count == 2:
            hotel_2_link = {
                "Link": hyperlink
            }
        if count == 3:
            hotel_3_link = {
                "Link": hyperlink
            }
            break
        
    hotel_1.update(hotel_1_price)
    hotel_2.update(hotel_2_price)
    hotel_3.update(hotel_3_price)
    hotel_1.update(hotel_1_link)
    hotel_2.update(hotel_2_link)
    hotel_3.update(hotel_3_link)

    hotel_options = {
        "hotel 1": hotel_1,
        "hotel 2": hotel_2,
        "hotel 3": hotel_3
    }

    return hotel_options
