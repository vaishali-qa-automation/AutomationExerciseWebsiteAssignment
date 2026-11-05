from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

AD_DOMAINS = [
    "*doubleclick.net*",
    "*googlesyndication.com*",
    "*googleadservices.com*",
    "*google-analytics.com*",
    "*googleads.g.doubleclick.net*",
    "*adservice.google.com*",
    "*pagead2.googlesyndication.com*",
    "*tpc.googlesyndication.com*",
    "*aswift_*",
    "*amazon-adsystem.com*",
    "*adnxs.com*",
    "*ads.yahoo.com*",
    "*adskeeper.co.uk*",
    "*adcolony.com*",
    "*outbrain.com*",
    "*taboola.com*",
    "*moatads.com*",
]

def _block_ads_via_cdp(driver):
    """Block ad domains using Chrome DevTools Protocol. Works on Chrome & Edge."""
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": AD_DOMAINS})

def _build_chrome_driver(headless=True):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)

    # CDP ad blocking
    _block_ads_via_cdp(driver)
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
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Edge(options=options)

    # CDP ad blocking
    _block_ads_via_cdp(driver)

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
