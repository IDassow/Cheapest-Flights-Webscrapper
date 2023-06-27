# original author credits https://github.com/Maximus-Alpha/tracking-cheap-flights/blob/main/13_Finding_Cheap_Flights.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
import time

import pandas as pd

import smtplib
from email.message import EmailMessage

import schedule

# departure_flight_inputs = {
#     "Departure": " JFK",
#     "Arrival": " LAX",
#     "Date": "Jun 20, 2021",
# }
# return_flight_inputs = {"Departure": " JFK", "Arrival": " ORD", "Date": "Aug 28, 2021"}


testFlightInfo = {
    "Departure": "Chicago, IL",
    "Arrival": "Los Angeles, CA",
    "Leave_Date": "Jul 20, 2023",
    "Return_Date": "Aug 5, 2023",
    "Trip_type": "Roundtrip",
    "Travelers": 1,
    "Airlines": ["AA"],
}


# self.infoDict = {
#             "Departure": self.locations_list[0],
#             "Arrival": self.locations_list[1],
#             "Leave_Date": self.dates_list[0],
#             "Return_Date": self.dates_list[1],
#             "Trip_type": self.filters_list[0],
#             "Travelers": self.filters_list[1],
#             "Airlines": self.filters_list[2],
#         }
def find_cheapest_flights(flight_info):
    PATH = "r'/projects/chromedriver"
    driver = webdriver.Chrome(executable_path=PATH)

    leaving_from = flight_info["Departure"]
    going_to = flight_info["Arrival"]
    start_date = flight_info["Leave_Date"]
    return_date = flight_info["Return_Date"]
    trip_type = flight_info["Trip_type"]
    travelers = flight_info["Travelers"]
    airlines_pref = flight_info["Airlines"]

    # Go to Expedia
    driver.get("https://expedia.com")

    # Click on Flights
    flight_xpath = '//a[@href="Flights"]'
    flight_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, flight_xpath))
    )
    flight_element.click()
    time.sleep(0.2)

    # Click on either One-Way or Round-Trip, there are more options but 2 is fine
    trip_type_xpath = ""
    if trip_type == "One-way":
        trip_type_xpath = '//a[@aria-controls="FlightSearchForm_ONE_WAY"]'
    else:
        trip_type_xpath = '//a[@aria-controls="FlightSearchForm_ROUND_TRIP"]'

    trip_type_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, trip_type_xpath))
    )
    trip_type_element.click()
    time.sleep(0.2)

    # Numbtravelers //button[@data-stid="open-room-picker"]

    # Part 1: Flying From, Flying To, Departure Date, Return Date

    # **********************  Complete Leaving From Portion  **********************
    leaving_from_xpath = '//button[@aria-label="Leaving from"]'
    leaving_from_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, leaving_from_xpath))
    )
    leaving_from_element.clear
    leaving_from_element.click()
    time.sleep(1)
    leaving_from_element.send_keys(leaving_from)

    time.sleep(1)  # Need this otherwise it will be too fast for the broswer
    leaving_from_element.send_keys(Keys.DOWN, Keys.RETURN)
    # **********************  Complete Leaving From Portion  **********************

    # **********************  Complete Going To Portion  **********************
    going_to_xpath = '//button[@aria-label="Going to"]'
    going_to_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, going_to_xpath))
    )
    going_to_element.clear
    going_to_element.click()
    time.sleep(1)
    going_to_element.send_keys(going_to)

    time.sleep(1)  # Need this otherwise it will be too fast for the broswer
    going_to_element.send_keys(
        Keys.DOWN, Keys.RETURN
    )  # Go down on item and click on it
    # **********************  Complete Going To Portion  **********************

    # **********************  Complete Departure Date(s) Portion  **********************

    departing_box_xpath = '//button[@data-stid="open-date-picker"]'

    depart_box_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, departing_box_xpath))
    )

    depart_box_element.click()  # Click on the departure box
    time.sleep(2)
    departing_date_element = ""
    return_date_element = ""

    if trip_type == "One-way":
        trip_date_xpath = '//button[contains(@aria-label,"{}")]'.format(start_date)
        while departing_date_element == "":
            try:
                departing_date_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, trip_date_xpath))
                )
                departing_date_element.click()  # Click on the departure date
            except TimeoutException:
                departing_date_element = ""
                next_month_xpath = '//button[@data-stid="date-picker-paging"][2]'
                driver.find_element_by_xpath(next_month_xpath).click()
                time.sleep(1)
        depart_date_done_xpath = '//button[@data-stid="apply-date-picker"]'
        driver.find_element_by_xpath(depart_date_done_xpath).click()

    else:
        start_date_xpath = '//button[contains(@aria-label,"{}")]'.format(start_date)
        return_date_xpath = '//button[contains(@aria-label,"{}")]'.format(return_date)
        while departing_date_element == "":
            try:
                departing_date_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, start_date_xpath))
                )
                departing_date_element.click()  # Click on the departure date
            except TimeoutException:
                departing_date_element = ""
                next_month_xpath = '//button[@data-stid="date-picker-paging"][2]'
                driver.find_element_by_xpath(next_month_xpath).click()
                time.sleep(1)

        while return_date_element == "":
            try:
                return_date_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, return_date_xpath))
                )
                return_date_element.click()  # Click on the departure date

            except TimeoutException:
                return_date_element = ""
                next_month_xpath = '//button[@data-stid="date-picker-paging"][2]'
                driver.find_element_by_xpath(next_month_xpath).click()
                time.sleep(1)

        depart_date_done_xpath = '//button[@data-stid="apply-date-picker"]'
        driver.find_element_by_xpath(depart_date_done_xpath).click()
    time.sleep(1)
    # **********************  Complete Departure Date Portion  **********************
    # Numbtravelers
    if travelers > 1:
        travelers_xpath = '//button[@data-stid="open-room-picker"]'
        traveler_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, travelers_xpath))
        )
        traveler_element.click()
        time.sleep(0.2)
        travelersNUM_xpath = "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[5]/div[1]/div/div/div/div[2]/form/div/div/div[3]/div/div[2]/div/div/section/div[1]/div/div/button[2]"
        travelerNUM_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, travelersNUM_xpath))
        )
        i = 1
        while i != travelers:
            travelerNUM_element.click()
            time.sleep(0.1)
            i += 1
        done_button_xpath = '//button[@id="travelers_selector_done_button"]'
        driver.find_element_by_xpath(search_button_xpath).click()
        time.sleep(0.5)

    # **********************  Click Search  **********************
    search_button_xpath = '//button[@data-testid="submit-button"]'
    driver.find_element_by_xpath(search_button_xpath).click()
    time.sleep(15)  # Need to let the page load properly
    # **********************  Click Search  **********************

    # Part 2: Setting Conditions for our flight

    # **********************  Check for Nonstop Flights Sorted by Lowest Price  **********************
    nonstop_flight_xpath = '//input[@id="stops-0"]'
    one_stop_flight_xpath = '//input[@id="stops-1"]'

    for airlines in airlines_pref:
        airlines_flight_xpath = '//input[@value="{}"]'.format(airlines)
        if len(driver.find_elements_by_xpath(airlines_flight_xpath)) > 0:
            driver.find_element_by_xpath(airlines_flight_xpath).click()
            time.sleep(5)

    if testFlightInfo["Trip_type"] == "One-Way":
        driver.find_element_by_xpath(nonstop_flight_xpath).click()
        time.sleep(5)

        # Check if there are available flights
        available_flights = driver.find_elements_by_xpath(
            "//span[contains(text(),'Select and show fare information ')]"
        )
        if len(available_flights) > 0:
            if len(available_flights) == 1:  # Don't have to sort by prices here
                flights = [
                    (
                        item.text.split(",")[0].split("for")[-1].title(),
                        item.text.split(",")[1].title().replace("At", ":"),
                        item.text.split(",")[2].title().replace("At", ":"),
                        item.text.split(",")[3].title().replace("At", ":"),
                    )
                    for item in available_flights[0:5]
                ]

            else:
                # Sort by lowest prices
                driver.find_element_by_xpath(
                    '//option[@data-opt-id="PRICE_INCREASING"]'
                ).click()
                time.sleep(5)
                flights = [
                    (
                        item.text.split(",")[0].split("for")[-1].title(),
                        item.text.split(",")[1].title().replace("At", ":"),
                        item.text.split(",")[2].title().replace("At", ":"),
                        item.text.split(",")[3].title().replace("At", ":"),
                    )
                    for item in available_flights[0:5]
                ]

            print(
                "Conditions satisfied for: {}:{}, {}:{}, {}:{}".format(
                    "Departure", leaving_from, "Arrival", going_to, "Date", start_date
                )
            )
            driver.quit()
            return flights

    # Roundtrips are difficult, we need to select the flight departing date
    # and then redo the filters for returning for one single entery.
    elif testFlightInfo["Trip_type"] == "Roundtrip":
        available_flights = driver.find_elements_by_xpath(
            "//span[contains(text(),'Select and show fare information ')]"
        )
        if len(available_flights) > 0:
            if len(available_flights) != 1:  # Don't have to sort by prices here
                driver.find_element_by_xpath(
                    '//option[@data-opt-id="PRICE_INCREASING"]'
                ).click()
                time.sleep(5)

                # Sort by lowest prices

            flights = []
            for item in available_flights[0:5]:
                flights.append(
                    item.text.split(",")[0].split("for")[-1].title(),
                    item.text.split(",")[1].title().replace("At", ":"),
                    item.text.split(",")[2].title().replace("At", ":"),
                    item.text.split(",")[3].title().replace("At", ":"),
                )
                print(
                    "Conditions satisfied for: {}:{}, {}:{}, {}:{}".format(
                        "Departure",
                        leaving_from,
                        "Arrival",
                        going_to,
                        "Date",
                        start_date,
                    )
                )

                i_xpath = '//button[@data-stid="FLIGHTS_DETAILS_AND_FARES-index-{}-leg-0-fsr-FlightsActionButton"]'.format(
                    item.iter
                )
                index_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, i_xpath))
                )

                index_element.click()  # Click on current flight
                # /html/body/div[2]/div[1]/div/div[2]/div[3]/div[1]/div/div[2]/main/ul/li[1]/div/div/div[1]/section/div[2]/div/div/div/div[4]/div/div/div[1]/ul/li[1]/div/div/div[4]/div[2]/button
                time.sleep(2)

                item_box_xpath = "/html/body/div[2]/div[1]/div/div[2]/div[3]/div[1]/div/div[2]/main/ul/li[1]/div/div/div[1]/section/div[2]/div/div/div/div[4]/div/div/div[1]/ul/li[1]/div/div/div[4]/div[2]/button"
                select_continue_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, item_box_xpath))
                )

                select_continue_element.click()  # Click on the select to continue to returning flights
                for airlines in airlines_pref:
                    airlines_flight_xpath = '//input[@value="{}"]'.format(airlines)
                    if len(driver.find_elements_by_xpath(airlines_flight_xpath)) > 0:
                        driver.find_element_by_xpath(airlines_flight_xpath).click()
                        time.sleep(5)

                flights.append
                (
                    item.text.split(",")[0].split("for")[-1].title(),
                    item.text.split(",")[1].title().replace("At", ":"),
                    item.text.split(",")[2].title().replace("At", ":"),
                    item.text.split(",")[3].title().replace("At", ":"),
                )
                print(
                    "Conditions satisfied for: {}:{}, {}:{}, {}:{}".format(
                        "Departure",
                        leaving_from,
                        "Arrival",
                        going_to,
                        "Date",
                        return_date,
                    )
                )
                return_back_xpath = "/html/body/div[2]/div[1]/div/div[2]/div[3]/div[1]/div/div[2]/main/section/div/div/ul/li[1]/div/a"
                return_back_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, return_back_xpath))
                )

                return_back_element.click()  # Click on the departure box

            driver.quit()
            return flights
    else:
        print(
            'Not all conditions could be met for the following: "{}:{}, {}:{}, {}:{}'.format(
                "Departure", leaving_from, "Arrival", going_to, "Date", start_date
            )
        )
        driver.quit()
        return []


def send_email():
    # Get return values
    testInfo = find_cheapest_flights(testFlightInfo)

    # Put it into a dataframe to visualize this more easily
    df = pd.DataFrame(testInfo)

    if not df.empty:  # Only send an email if we have actual flight info
        email = open("none56242@gmail.com").read()
        password = open("ThrowAway4T3sting").read()

        msg = EmailMessage()

        msg[
            "Subject"
        ] = "Python Flight Info! {} --> {}, Departing: {}, Returning: {}".format(
            testInfo["Departure"],
            testInfo["Arrival"],
            testInfo["Leave_Date"],
            testInfo["Return_Date"],
        )

        msg["From"] = email
        msg["To"] = email

        msg.add_alternative(
            """\
            <!DOCTYPE html>
            <html>
                <body>
                    {}
                </body>
            </html>""".format(
                df.to_html()
            ),
            subtype="html",
        )

        with smtplib.SMTP_SSL("Email server name here", 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)


# schedule.clear()
# schedule.every(30).minutes.do(send_email)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
