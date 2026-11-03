from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def _build_chrome_driver(headless=True):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--no-first-run")
    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": [
            "*doubleclick.net*",
            "*googlesyndication.com*",
            "*googleadservices.com*",
            "*google-analytics.com*",
            "*googleads.g.doubleclick.net*",
            "*adservice.google.com*",
            "*pagead2.googlesyndication.com*",
            "*aswift_*",
            "*tpc.googlesyndication.com*",
            "*.amazon-adsystem.com*",
            "*.adnxs.com*",
        ]
    })
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
    options.add_argument("--start-maximized")
    options.add_argument("--no-first-run")
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
