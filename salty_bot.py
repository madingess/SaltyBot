import random
import time

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By

# Constants
TEAM_RED = "player1"
TEAM_BLUE = "player2"


class SaltyBot:
    def __init__(self, parameters, driver):
        self.browser = driver
        self.email = parameters['email']
        self.username = parameters['username']
        self.password = parameters['password']

    def login(self):
        """Login to SaltyBet"""
        try:
            self.browser.get("https://www.saltybet.com/authenticate?signin=1")
            time.sleep(random.uniform(5, 10))
            self.browser.find_element_by_id("email").send_keys(self.email)
            self.browser.find_element_by_id("pword").send_keys(self.password)
            self.browser.find_element_by_css_selector(".graybutton").click()
            time.sleep(random.uniform(5, 10))
        except TimeoutException:
            raise Exception("Could not login!")

    def continuous_betting(self):
        """Main operating loop to perform betting when available"""
        while True:
            if self.can_bet():
                # Select wager amount and team
                wager_amount = self.get_wager_amount()
                wager_team = self.select_wager_team()

                # Make wager
                self.browser.find_element_by_id("wager").clear()
                self.browser.find_element_by_id("wager").send_keys(wager_amount)
                self.browser.find_element_by_id(wager_team).click()
                print("Bet " + str(wager_amount) + " on " + wager_team)
            else:
                print("Ongoing fight. Cannot bet.")

            self.wait_to_wager()

    def can_bet(self):
        """Determine and return whether betting is open"""
        try:
            self.browser.find_element_by_id("wager").send_keys(0)
            return True
        except ElementNotInteractableException:
            return False

    def get_wager_amount(self):
        """Determine and return how many salty bucks to wager"""
        minimum = 100
        balance = self.get_balance()
        if balance < minimum:
            return balance
        return minimum

    def get_balance(self):
        """Find and return the current balance of Salty Bucks"""
        return int(self.browser.find_element(By.ID, "balance").get_attribute("innerHTML").replace(",", ""))

    def select_wager_team(self):
        """Determine and return which team on whom to wager"""
        return TEAM_RED

    def wait_to_wager(self):
        """
        Sleep to wait until betting is open.
        45 seconds are allowed for wagers between matches.
        25-30 sleep intervals will allow us to always bet once during wager openings.
        """
        sleep_time = random.uniform(25, 30)
        print("Sleeping for " + str(sleep_time) + " seconds")
        try:
            time.sleep(sleep_time)
        except TimeoutException:
            raise Exception("TimeoutException while waiting to wager")