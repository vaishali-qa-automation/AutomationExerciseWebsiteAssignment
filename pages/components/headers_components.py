import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePageClass

logger = logging.getLogger(__name__)


class HeaderComponentLocator:
    """Locators for navigation elements in the application header."""

    SIGNUP_AND_LOGIN_PAGE_NAV = (
        By.CSS_SELECTOR,
        "a[href='/login']",
    )
    PRODUCTS_VIEW_NAV = (
        By.CSS_SELECTOR,
        "a[href='/products']",
    )
    CART_VIEW_NAV = (
        By.CSS_SELECTOR,
        "a[href='/view_cart']",
    )
    LOGOUT_NAV = (
        By.CSS_SELECTOR,
        "a[href='/logout']",
    )
    DELETE_ACCOUNT_NAV = (
        By.CSS_SELECTOR,
        "a[href='/delete_account']",
    )
    LOGGED_IN_USER = (
        By.CSS_SELECTOR,
        "li > a > b"
    )


class HeaderComponentClass(BasePageClass):
    """Page component containing application header navigation methods."""

    def __init__(self, driver) -> None:
        """Initialize the header component.

        Args:
            driver: Selenium WebDriver instance used to interact with
                the application.
        """
        super().__init__(driver)

    def _navigate_to_page(self, locator) -> None:
        self.click_element(locator)

    def navigate_to_login_page(self) -> None:
        """Navigate to the login and signup page.

        The method clicks the Login/Signup navigation link and verifies
        that the browser URL contains ``/login``.

        Raises:
            TimeoutException: If the Login/Signup navigation element does
                not become available or the expected URL is not reached.
        """
        logger.info("Navigating to the Login/Signup page.")

        self._navigate_to_page(HeaderComponentLocator.SIGNUP_AND_LOGIN_PAGE_NAV)

        if self.wait_for_url_contains("/login"):
            logger.info("Successfully navigated to the Login/Signup page.")
        else:
            logger.warning("Failed to navigate to the Login/Signup page.")

    def navigate_to_products_page(self) -> None:
        """Navigate to the products page.

        The method clicks the Products navigation link and verifies that
        the browser URL contains ``/products``.

        Raises:
            TimeoutException: If the Products navigation element does not
                become available or the expected URL is not reached.
        """
        logger.info("Navigating to the Products page.")

        self._navigate_to_page(HeaderComponentLocator.PRODUCTS_VIEW_NAV)

        if self.wait_for_url_contains("/products"):
            logger.info("Successfully navigated to the Products page.")
        else:
            logger.warning("Failed to navigate to the Products page.")

    def navigate_to_cart_page(self) -> None:
        """Navigate to the shopping cart page.

        The method clicks the Cart navigation link and verifies that
        the browser URL contains ``/view_cart``.

        Raises:
            TimeoutException: If the Cart navigation element does not
                become available or the expected URL is not reached.
        """
        logger.info("Navigating to the Cart page.")

        self._navigate_to_page(HeaderComponentLocator.CART_VIEW_NAV)

        if self.wait_for_url_contains("/view_cart"):
            logger.info("Successfully navigated to the Cart page.")
        else:
            logger.warning("Failed to navigate to the Cart page.")

    def logout(self) -> None:
        """Log out the currently authenticated user.

        The method clicks the Logout navigation link and verifies that
        the browser is redirected to the login page.

        Raises:
            TimeoutException: If the Logout navigation element does not
                become available or the expected URL is not reached.
        """
        logger.info("Logging out the current user.")

        self._navigate_to_page(HeaderComponentLocator.LOGOUT_NAV)

        if self.wait_for_url_contains("/login"):
            logger.info("Successfully logged out the user.")
        else:
            logger.warning("Failed to verify logout navigation.")

    def get_logged_in_user_name(self):
        logged_in = self.locate_element(
            HeaderComponentLocator.LOGGED_IN_USER
        )
        return logged_in.text

    def delete_account(self):
        """
        This method will delete the account of current user
        Raises:
            TimeoutException: If the delete account navigation element does not
                become available or the expected URL is not reached.
        """
        logger.info("Clicking on Delete Account")
        self._navigate_to_page(
            HeaderComponentLocator.DELETE_ACCOUNT_NAV
        )
        if self.wait_for_url_contains("/delete_account"):
            logger.info("Successfully deleted the user account.")
        else:
            logger.warning(
                "Failed to delete user account."
            )
