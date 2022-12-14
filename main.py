import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from validate_email import validate_email
from salty_bot import SaltyBot, WAGER_STRATEGIES


def init_browser():
    browser_options = Options()
    options = ['--disable-blink-features', '--no-sandbox', '--disable-extensions',
               '--ignore-certificate-errors', '--disable-blink-features=AutomationControlled']
    for option in options:
        browser_options.add_argument(option)

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=browser_options)
    driver.set_window_position(0, 0)
    driver.maximize_window()
    return driver


def get_configuration():
    """
    Get input from configuration file and validate values.
    Return valid configuration or raise exception.
    """
    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    mandatory_params = ['email', 'username', 'password', 'wager_strategy', 'constant_wager']
    for mandatory_param in mandatory_params:
        if mandatory_param not in parameters:
            raise Exception(mandatory_param + ' is not inside the yml file!')

    assert validate_email(parameters['email'])
    assert len(str(parameters['username'])) > 0
    assert len(str(parameters['password'])) > 0

    assert str(parameters['wager_strategy']) in WAGER_STRATEGIES
    assert int(parameters['constant_wager']) > 0
    assert parameters['percentage_wager'] > 0
    assert parameters['percentage_wager'] < 1

    return parameters


if __name__ == '__main__':
    parameters = get_configuration()
    browser = init_browser()

    bot = SaltyBot(parameters, browser)
    bot.login()
    bot.continuous_betting()
