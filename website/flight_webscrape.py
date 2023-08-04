from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re


def FlightScraper(start_input, destination_input, departure_date, return_date, seat):

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
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

    url = 'https://www.google.com/travel/flights/search?tfs=CBwQAhonEgoyMDIzLTA5LTAyagwIAxIIL20vMGYyczZyCwgCEgcvbS8wdnptQAFIAXABggELCP___________wGYAQI&hl=en-US&curr=USD'
    driver.get(url)

    if seat != "Economy":
        seat_quality = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div/div[1]'
        element = (By.XPATH, seat_quality)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

        if seat == "Premium Economy":
            seat_choice = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div/div[2]/ul/li[2]'
            element = (By.XPATH, seat_choice)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

        if seat == "Business":
            seat_choice = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div/div[2]/ul/li[3]'
            element = (By.XPAT, seat_choice)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

        if seat == "First":
            seat_choice = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div/div[2]/ul/li[4]'
            element = (By.XPATH, seat_choice)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

        element = (By.XPATH, seat_quality)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

    box_start = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input'
    element = (By.XPATH, box_start)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

    start_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'
    element = (By.XPATH, start_text)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(start_input + '\n')

    box_destination = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input'
    element = (By.XPATH, box_destination)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

    destination_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'
    element = (By.XPATH, destination_text)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(destination_input + '\n')

    departure_date_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input'
    element = (By.XPATH, departure_date_text)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(departure_date + '\n')

    time.sleep(4)

    # Extracting departure flight options

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    count = 0

    flights = soup.find_all("li", class_="pIav2d")
    for flight in flights:
        description = flight.find("div", class_='JMc5Xc').get("aria-label")
        
        cost_match = re.search(r'\bFrom (\d+) US dollars', description)
        cost_of_flight_first = int(cost_match.group(1))

        # Extracting the airline
        airline_match = re.search(r'with (\w+)', description)
        airline_first = airline_match.group(1)

        # Extracting the departure and arrival airports
        departure_match = re.search(r'Leaves (.+?) at', description)
        departure_airport_first = departure_match.group(1).strip()

        arrival_match = re.search(r'arrives at (.+?)\.', description)
        arrival_airport_first = arrival_match.group(1).strip()

        # Extracting the departure and arrival times
        departure_time_match = re.search(r'at (\d+:\d+ (?:AM|PM))', description)
        departure_time_first = departure_time_match.group(1)

        arrival_string_match = re.search(r'arrives at (.+?\.)', description)
        arrival_string = arrival_string_match.group(1)

        arrival_time_match = re.search(r'at (\d+:\d+ (?:AM|PM))', arrival_string)
        arrival_time_first = arrival_time_match.group(1)

        # Extracting the duration of the flight
        duration_match = re.search(r'Total duration (\d+) hr (\d+) min', description)
        duration_hours = int(duration_match.group(1))
        duration_minutes = int(duration_match.group(2))

        # Convert duration to string format (e.g., "3 hr 8 min")
        duration_string_first = f"{duration_hours} hr {duration_minutes} min"  

        print(description)
        count += 1
        if count == 1:
            flight_info_1 = {
            "first cost": cost_of_flight_first,
            "first airline": airline_first,
            "first departure airport": departure_airport_first,
            "first arrival airport": arrival_airport_first,
            "first departure time": departure_time_first, 
            "first arrival time": arrival_time_first,
            "first duration": duration_string_first,
            }
        if count == 2:
            flight_info_2 = {
            "first cost": cost_of_flight_first,
            "first airline": airline_first,
            "first departure airport": departure_airport_first,
            "first arrival airport": arrival_airport_first,
            "first departure time": departure_time_first, 
            "first arrival time": arrival_time_first,
            "first duration": duration_string_first,
            }
        if count == 3:
            flight_info_3 = {
            "first cost": cost_of_flight_first,
            "first airline": airline_first,
            "first departure airport": departure_airport_first,
            "first arrival airport": arrival_airport_first,
            "first departure time": departure_time_first, 
            "first arrival time": arrival_time_first,
            "first duration": duration_string_first,
            }
            break

    switch_flights = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[3]/button'
    element = (By.XPATH, switch_flights)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

    departure_date_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input'
    element = (By.XPATH, departure_date_text)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(return_date + '\n')

    time.sleep(4)

    count = 0

    new_url = driver.current_url
    driver.get(new_url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    # Extracting return flight options

    flights = soup.find_all("li", class_="pIav2d")
    for flight in flights:
        description = flight.find("div", class_='JMc5Xc').get("aria-label")

        cost_match = re.search(r'\bFrom (\d+) US dollars', description)
        cost_of_flight_second = int(cost_match.group(1))

        # Extracting the airline
        airline_match = re.search(r'with (\w+)', description)
        airline_second = airline_match.group(1)

        # Extracting the departure and arrival airports
        departure_match = re.search(r'Leaves (.+?) at', description)
        departure_airport_second = departure_match.group(1).strip()

        arrival_match = re.search(r'arrives at (.+?)\.', description)
        arrival_airport_second = arrival_match.group(1).strip()

        # Extracting the departure and arrival times
        departure_time_match = re.search(r'at (\d+:\d+ (?:AM|PM))', description)
        departure_time_second = departure_time_match.group(1)

        arrival_string_match = re.search(r'arrives at (.+?\.)', description)
        arrival_string = arrival_string_match.group(1)

        arrival_time_match = re.search(r'at (\d+:\d+ (?:AM|PM))', arrival_string)
        arrival_time_second = arrival_time_match.group(1)

        # Extracting the duration of the flight
        duration_match = re.search(r'Total duration (\d+) hr (\d+) min', description)
        duration_hours = int(duration_match.group(1))
        duration_minutes = int(duration_match.group(2))

        # Convert duration to string format (e.g., "3 hr 8 min")
        duration_string_second = f"{duration_hours} hr {duration_minutes} min"

        print(description)
        
        count += 1

        if count == 1:
            flight_info_4 = {
                "second cost": cost_of_flight_second,
                "second airline": airline_second,
                "second departure airport": departure_airport_second,
                "second arrival airport": arrival_airport_second,
                "second departure time": departure_time_second, 
                "second arrival time": arrival_time_second,
                "second duration": duration_string_second,
            }
        if count == 2:
            flight_info_5 = {
                "second cost": cost_of_flight_second,
                "second airline": airline_second,
                "second departure airport": departure_airport_second,
                "second arrival airport": arrival_airport_second,
                "second departure time": departure_time_second, 
                "second arrival time": arrival_time_second,
                "second duration": duration_string_second,
            }
        if count == 3:
            flight_info_6 = {
                "second cost": cost_of_flight_second,
                "second airline": airline_second,
                "second departure airport": departure_airport_second,
                "second arrival airport": arrival_airport_second,
                "second departure time": departure_time_second, 
                "second arrival time": arrival_time_second,
                "second duration": duration_string_second,
            }
            break
        
    flight_info_1.update(flight_info_4)

    flight_info_2.update(flight_info_5)

    flight_info_3.update(flight_info_6)

    flight_info = {
        "flight 1": flight_info_1,
        "flight 2": flight_info_2,
        "flight 3": flight_info_3,
    }

    return flight_info