import logging
from typing import Any

from selenium.common import (
    StaleElementReferenceException,
    TimeoutException, ElementClickInterceptedException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from utilities.decorators import (
    logging_decorator,
    retry_on_exception,
)

logger = logging.getLogger(__name__)


class BasePageClass:
    """Base framework class providing automated browser interaction helpers."""

    def __init__(self, driver: Any) -> None:
        """Initializes BaseClass with a Selenium WebDriver instance.

        Args:
            driver: The Selenium WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=5)

    @logging_decorator
    def navigate_to_url(self, url: str):
        """
        This method navigates to the given url and also waits until the url appears
        Args:
            url: Url to navigate to

        Returns: None

        """
        self.driver.get(url)
        if self.wait.until(EC.url_to_be(url)):
            logger.info(f"Successfully navigated to {url}")
        else:
            logger.info(f"Failed to navigated to {url}")

    @logging_decorator
    def locate_element(self, locator: tuple[str, str]) -> WebElement:
        """Waits for an element to be present and visible in the DOM.

        Args:
            locator: A tuple containing the locator strategy and target value.
        """
        self.wait.until(EC.presence_of_element_located(locator))
        elem = self.wait.until(EC.visibility_of_element_located(locator))
        return elem

    @logging_decorator
    @retry_on_exception(
        times=2, delay=0.2, exceptions=(StaleElementReferenceException,)
    )
    def click_element(self, locator: tuple[str, str]) -> None:
        """
        Waits for an element to be clickable by its locator and clicks it.
        Args:
            locator: locator to locate element and click it

        Returns: None

        """
        webdriver_wait = WebDriverWait(self.driver, timeout=20)
        element = webdriver_wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @logging_decorator
    @retry_on_exception(
        times=2, delay=0.2, exceptions=(StaleElementReferenceException,)
    )
    def enter_text(self, locator: tuple[str, str], text: str) -> None:
        """
        Wait for an input element, clear it, and enter text using its locator.
        Args:
            locator: locator to locate element and enter text.
            text: text to enter

        Returns: None

        """
        # Click using the locator to prevent stale element issues
        self.click_element(locator)

        # Grab the fresh element reference to interact with it directly
        element = self.locate_element(locator)
        element.clear()
        element.send_keys(text)

    @logging_decorator
    def wait_for_element_to_be_clickable(
        self,
        element: WebElement,
    ) -> None:
        """Wait until an element becomes clickable.

        Args:
            element: Selenium WebElement to wait for.

        Raises:
            TimeoutException: If the element does not become clickable within
                the configured timeout.
        """
        self.wait.until(EC.element_to_be_clickable(element))

    @logging_decorator
    def is_element_visible(self, locator: tuple[str, str], timeout: int = 3) -> bool:
        """Safely checks if an element is visible within a specific timeout.

        Returns:
            bool: True if visible within timeout, False otherwise.
        """
        try:
            # Instantiate a localized wait using the custom timeout parameter
            local_wait = WebDriverWait(self.driver, timeout=timeout)
            local_wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @logging_decorator
    def is_element_invisible(self, locator: tuple[str, str], timeout: int = 3) -> bool:
        """Safely checks if an element is invisible or missing within a specific timeout.

        Returns:
            bool: True if invisible/absent within timeout, False otherwise.
        """
        try:
            local_wait = WebDriverWait(self.driver, timeout=timeout)
            local_wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @logging_decorator
    def wait_for_url_contains(self, url_substring: str, timeout: int = 5) -> bool:
        """Waits until the current browser URL contains the given substring.

        Returns:
            bool: True if condition is met, False if it times out.
        """
        try:
            local_wait = WebDriverWait(self.driver, timeout=timeout)
            local_wait.until(EC.url_contains(url_substring))
            return True
        except TimeoutException:
            return False

    @logging_decorator
    def wait_for_exact_url(self, expected_url: str, timeout: int = 5) -> bool:
        """Waits until the current browser URL exactly matches the given string.

        Returns:
            bool: True if condition is met, False if it times out.
        """
        try:
            local_wait = WebDriverWait(self.driver, timeout=timeout)
            local_wait.until(EC.url_to_be(expected_url))
            return True
        except TimeoutException:
            return False

    @logging_decorator
    def select_option(
        self, locator: tuple[str, str], value: str | int, by: str = "text"
    ) -> None:
        """Selects an option from a standard HTML <select> dropdown element.

        Args:
            locator: A tuple containing the locator strategy and target value
                (e.g., `(By.ID, "country-dropdown")`).
            value: The target string (for 'text' or 'value') or integer (for 'index')
                to select.
            by: Selection strategy to use. Options are:
                - `"text"` (default): Matches visible text of the option.
                - `"value"`: Matches the HTML 'value' attribute of the option.
                - `"index"`: Matches zero-based index of the option.

        Raises:
            ValueError: If an invalid `by` strategy is provided or value type mismatches.
            NoSuchElementException: If the element or target option isn't found.
            UnexpectedTagNameException: If target element isn't an HTML `<select>`.
        """
        # 1. Wait until dropdown element is present and visible
        dropdown_element = self.locate_element(locator)

        # 2. Wrap element in Selenium's Select wrapper class
        select = Select(dropdown_element)

        # 3. Perform selection based on passed strategy
        strategy = by.lower()
        if strategy == "text":
            select.select_by_visible_text(str(value))
        elif strategy == "value":
            select.select_by_value(str(value))
        elif strategy == "index":
            if not isinstance(value, int):
                raise ValueError(
                    f"Selection strategy 'index' requires an integer value, got {type(value)}"
                )
            select.select_by_index(value)
        else:
            raise ValueError(
                f"Invalid selection strategy '{by}'. Use 'text', 'value', or 'index'."
            )
