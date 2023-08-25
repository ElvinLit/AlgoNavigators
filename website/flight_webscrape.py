from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re


def FlightScraper(start_input, destination_input, departure_date, return_date, seat):

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
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

    start_loop = False

    while start_loop == False:
    
        try:
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

                '''element = (By.XPATH, seat_quality)
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()'''

        except TimeoutException:
            print("Couldn't click out of seat selection! (TimeoutException)")
            print("Trying Again, Please Wait...")
            continue
            
        except ElementClickInterceptedException:
            print("Couldn't click out of seat selection! (ElementClickInterceptedException)")
            print("Trying Again, Please Wait...")
            continue

        try:
            box_start = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input'
            element = driver.find_element(By.XPATH, box_start)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).clear()
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(start_input)

            start_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]'
            element = (By.XPATH, start_text)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

        except TimeoutException:
            print("Couldn't click starting destination! (TimeoutException)")
            print("Trying Again, Please Wait...")
            continue
            
        except ElementClickInterceptedException:
            print("Couldn't click starting destination! (ElementClickInterceptedException)")
            print("Trying Again, Please Wait...")
            continue

        try:
            box_destination = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input'
            element = (By.XPATH, box_destination)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).clear()
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(destination_input + '\n')

            destination_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]'
            element = (By.XPATH, destination_text)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

            departure_date_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input'
            element = (By.XPATH, departure_date_text)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(departure_date + '\n')
        
        except TimeoutException:
            print("Couldn't click final destination! (TimeoutException)")
            print("Trying Again, Please Wait...")
            continue
            
        except ElementClickInterceptedException:
            print("Couldn't click final destination! (ElementClickInterceptedException)")
            print("Trying Again, Please Wait...")
            continue

        no_flight = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div[1]/h3'

        try:
            element = (By.XPATH, no_flight)
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable(element)).click()
            print("There are no flights!")
            break
        
        except NoSuchElementException and TimeoutException:
            print("There are flights!")

        start_loop = True

    #Makes sure page is loaded before beautiful soup is activated
    page_body = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]'
    element = (By.XPATH, page_body)
    WebDriverWait(driver, 3).until(EC.presence_of_element_located(element))

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    count = 0

    flights = soup.find_all("li", class_="pIav2d")
    for i in range(0, 3):
        elements = driver.find_elements(By.CLASS_NAME, "pIav2d")
        count_1 = 0 

        for elemen in elements:
            pagenew = ""
            if count_1 == i:
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable(elemen)).click()
                pagenew = driver.current_url
                time.sleep(0.5)
                driver.back()
                time.sleep(0.5)
                if count_1 == 0:
                    flight_info_1_5 ={
                        "first link": pagenew
                    }
                if count_1 == 1:
                    flight_info_2_5 ={
                        "first link": pagenew
                    }

                if count_1 == 2:
                    flight_info_3_5 ={
                        "first link": pagenew
                    }
                
            count_1 += 1
 

    #Makes sure page is loaded before beautiful soup is activated
    page_body = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]'
    element = (By.XPATH, page_body)
    WebDriverWait(driver, 3).until(EC.presence_of_element_located(element))

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

        arrival_string_match = re.search(r'arrives at (.+?) Total', description)
        arrival_string = arrival_string_match.group(1)

        arrival_time_match = re.search(r'at (\d+:\d+ (?:AM|PM))', arrival_string)

        arrival_time_first = arrival_time_match.group(1)

        # Extracting the duration of the flight
        try:
            duration_match = re.search(r'duration (\d+) hr (\d+) min', description)
            duration_hours = int(duration_match.group(1))
            duration_minutes = int(duration_match.group(2))
            
            # Convert duration to string format (e.g., "3 hr 8 min")
            duration_string_first = f"{duration_hours} hr {duration_minutes} min"
        except AttributeError:
            duration_match = re.search(r'duration (\d+) hr', description)
            duration_hours = int(duration_match.group(1))

            # Convert duration to string format (e.g., "3 hr")
            duration_string_first = f"{duration_hours} hr"

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

    flight_info_1.update(flight_info_1_5)
    flight_info_2.update(flight_info_2_5)
    flight_info_3.update(flight_info_3_5)

    pagenew = driver.current_url

    return_loop = True

    while return_loop == True:

        try:
            driver.get(pagenew)
            switch_flights = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[3]/button'
            element = (By.XPATH, switch_flights)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

            departure_date_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input'
            element = (By.XPATH, departure_date_text)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(return_date + '\n')

            return_loop = False

        except TimeoutException:
            print("Couldn't switch to return flight! (TimeoutException)")
            print("Trying Again, Please Wait...")
            continue
                
        except ElementClickInterceptedException:
            print("Couldn't switch to return flight! (ElementClickInterceptedException)")
            print("Trying Again, Please Wait...")
            continue

    #Makes sure page is loaded before beautiful soup is activated
    time.sleep(2)
    #Need to find something that is different from one page versus another...

    for i in range(0, 3):
        elements = driver.find_elements(By.CLASS_NAME, "pIav2d")
        count_1 = 0 

        for elemen in elements:
            pagenew = ""
            if count_1 == i:
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable(elemen)).click()
                pagenew = driver.current_url
                time.sleep(0.5)
                driver.back()
                time.sleep(0.5)
                if count_1 == 0:
                    flight_info_4_5 ={
                        "second link": pagenew
                    }
                if count_1 == 1:
                    flight_info_5_5 ={
                        "second link": pagenew
                    }
                if count_1 == 2:
                    flight_info_6_5 ={
                        "second link": pagenew
                    }

            count_1 += 1

    #Makes sure page is loaded before beautiful soup is activated
    page_body = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]'
    element = (By.XPATH, page_body)
    WebDriverWait(driver, 3).until(EC.presence_of_element_located(element))

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

        arrival_match = re.search(r'arrives at (.+?)\ at', description)
        arrival_airport_second = arrival_match.group(1).strip()

        # Extracting the departure and arrival times
        departure_time_match = re.search(r'at (\d+:\d+ (?:AM|PM))', description)
        departure_time_second = departure_time_match.group(1)

        arrival_string_match = re.search(r'arrives at (.+?) Total', description)
        arrival_string = arrival_string_match.group(1)

        arrival_time_match = re.search(r'at (\d+:\d+ (?:AM|PM))', arrival_string)
        arrival_time_second = arrival_time_match.group(1)

        # Extracting the duration of the flight
        try:
            duration_match = re.search(r'duration (\d+) hr (\d+) min', description)
            duration_hours = int(duration_match.group(1))
            duration_minutes = int(duration_match.group(2))
            
            # Convert duration to string format (e.g., "3 hr 8 min")
            duration_string_second = f"{duration_hours} hr {duration_minutes} min"
        except AttributeError:
            duration_match = re.search(r'duration (\d+) hr', description)
            duration_hours = int(duration_match.group(1))

            # Convert duration to string format (e.g., "3 hr")
            duration_string_second = f"{duration_hours} hr"
 
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

    flight_info_4.update(flight_info_4_5)
    flight_info_5.update(flight_info_5_5)
    flight_info_6.update(flight_info_6_5)

    flight_info_1.update(flight_info_4)

    flight_info_2.update(flight_info_5)

    flight_info_3.update(flight_info_6)

    flight_info = {
        "flight 1": flight_info_1,
        "flight 2": flight_info_2,
        "flight 3": flight_info_3,
    }

    driver.close()

    return flight_info