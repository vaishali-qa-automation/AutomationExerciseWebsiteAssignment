import logging
from typing import Any, Union

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from utilities.decorators import (
    logging_decorator,
    retry_on_exception, retry_on_condition,
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
    @retry_on_exception(times=3, delay=0.2)
    def locate_element(self, locator: tuple[str, str]) -> WebElement:
        """Waits for an element to be present and visible in the DOM.

        Args:
            locator: A tuple containing the locator strategy and target value
                (e.g., `(By.XPATH, "//div")`).

        Returns:
            WebElement: The located and visible Selenium WebElement.

        Raises:
            TimeoutException: If the element is not found/visible within timeout limits.
        """
        self.wait.until(EC.presence_of_element_located(locator))
        self.wait.until(EC.visibility_of_element_located(locator))
        elem = self.driver.find_element(*locator)
        return elem

    @logging_decorator
    def click_element(self, element: WebElement):
        try:
            self.wait_for_element_to_be_clickable(element)
            element.click()
        except ElementClickInterceptedException:
            logger.error("Element click was intercepted and failed to click")

    @logging_decorator
    def enter_text(self, locator, text: str) -> None:
        """Wait for an input element and enter the provided text.

        Args:
            locator: Selenium locator tuple used to find the input element.
            text: Text to enter into the input element.
        """
        element = self.locate_element(locator)
        self.click_element(element)
        element.clear()
        element.send_keys(text)

    @logging_decorator
    @retry_on_exception(times=3, delay=0.2)
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
    @retry_on_condition(delay=0.1)
    def is_element_invisible(self, element: WebElement) -> bool:
        """
        This method checks if element is invisible or not.
        Args:
            element: WebElement to check for invisible.

        Returns: True or False
        """
        result = self.wait.until(EC.invisibility_of_element(element))
        if isinstance(result, WebElement):
            return False
        return True

    @logging_decorator
    @retry_on_condition(delay=0.1)
    def is_element_visible(self, element: WebElement) ->  bool:
        """
        This method checks for visibility of an element and returns WebElement or False.
        Args:
            element: WebElement to check for visibility.

        Returns: bool or WebElement

        """
        result = self.wait.until(EC.visibility_of(element))
        if isinstance(result, WebElement):
            return True
        return False


    @logging_decorator
    @retry_on_condition(delay=0.1)
    def wait_for_url_contains(self, url_substring: str, timeout: int = 5) -> bool:
        """Waits until the current browser URL contains the given substring.

        Args:
            url_substring: Partial string expected to be in the URL.
            timeout: Maximum wait time in seconds.

        Returns:
            bool: True if the condition is met within the timeout.
        """

        return self.wait.until(EC.url_contains(url_substring))

    @logging_decorator
    @retry_on_condition(delay=0.1)
    def wait_for_exact_url(self, expected_url: str, timeout: int = 5) -> bool:
        """Waits until the current browser URL exactly matches the given string.

        Args:
            expected_url: The full expected URL.
            timeout: Maximum wait time in seconds.

        Returns:
            bool: True if the condition is met within the timeout.
        """
        return self.wait.until(EC.url_to_be(expected_url))


    @logging_decorator
    def select_option(
            self,
            locator:  tuple[str, str],
            value: Union[str, int],
            by: str = "text"
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
        if by == "text":
            select.select_by_visible_text(str(value))
        elif by == "value":
            select.select_by_value(str(value))
        elif by == "index":
            if not isinstance(value, int):
                raise ValueError(
                    f"Selection strategy 'index' requires an integer value, got {type(value)}"
                )
            select.select_by_index(value)
        else:
            raise ValueError(
                f"Invalid selection strategy '{by}'. Use 'text', 'value', or 'index'."
            )