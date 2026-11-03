from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def _build_chrome_driver(headless=True):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--maximize")
    driver = webdriver.Chrome(options=options)
    return driver


def _build_firefox_driver(headless=True):
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--maximize")
    driver = webdriver.Firefox(options=options)
    return driver


def _build_edge_driver(headless=True):
    options = EdgeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--maximize")
    driver = webdriver.Edge(options=options)
    return driver


def get_driver(browser, headless=True):
    if browser.lower().strip() == "chrome":
        return _build_chrome_driver(headless)
    elif browser.lower().strip() == "firefox":
        return _build_firefox_driver(headless)
    elif browser.lower().strip() == "edge":
        return _build_edge_driver(headless)
    else:
        raise ValueError("Invalid browser type")
