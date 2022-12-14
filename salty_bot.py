import random
import time

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By

# Constants
TEAM_RED = "player1"
TEAM_BLUE = "player2"

WAGER_STRATEGY_CONSTANT = "constant"
WAGER_STRATEGY_ALLIN = "all-in"
WAGER_STRATEGY_PERCENTAGE = "percentage"
WAGER_STRATEGIES = [
    WAGER_STRATEGY_CONSTANT,
    WAGER_STRATEGY_ALLIN,
    WAGER_STRATEGY_PERCENTAGE
]


class SaltyBot:
    def __init__(self, parameters, driver):
        self.browser = driver
        self.email = parameters['email']
        self.username = parameters['username']
        self.password = parameters['password']
        self.wager_strategy = parameters['wager_strategy']
        self.constant_wager = int(parameters['constant_wager'])
        self.percentage_wager = parameters['percentage_wager']

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
            if self.can_bet() and not self.bet_placed():
                # Select wager amount and team
                wager_amount = self.get_wager_amount()
                wager_team = self.select_wager_team()

                # Make wager
                self.browser.find_element_by_id("wager").clear()
                self.browser.find_element_by_id("wager").send_keys(wager_amount)
                self.browser.find_element_by_id(wager_team).click()
                print("Bet " + str(wager_amount) + " on " + wager_team)
            else:
                print("Ongoing fight or bet already placed. Cannot bet.")

            self.wait_to_wager()

    def can_bet(self):
        """Determine and return whether betting is open"""
        return "display: none" not in self.browser.find_element_by_id("wager").get_attribute('style')

    def bet_placed(self):
        """Determine and return whether a bet has been placed"""
        try:
            self.browser.find_element_by_id("betconfirm")
            return True
        except ElementNotInteractableException:
            return False

    def get_wager_amount(self):
        """Determine and return how many salty bucks to wager"""
        strategies = {
            WAGER_STRATEGY_CONSTANT: self.wager_strategy_constant(),
            WAGER_STRATEGY_ALLIN: self.wager_strategy_allin(),
            WAGER_STRATEGY_PERCENTAGE: self.wager_strategy_percentage()
        }
        return strategies.get(self.wager_strategy, self.wager_strategy_constant())  # default to constant strategy

    def wager_strategy_constant(self):
        """Wager a constant value. All-in if balance is lower than constant value"""
        balance = self.get_balance()
        if balance < self.constant_wager:
            return balance
        return self.constant_wager

    def wager_strategy_allin(self):
        """Wager full balance."""
        return self.get_balance()

    def wager_strategy_percentage(self):
        """Wager a percentage of the account balance."""
        return int(self.get_balance() * self.percentage_wager)

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
