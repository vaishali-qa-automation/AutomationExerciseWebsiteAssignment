import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePageClass

logger = logging.getLogger(__name__)


class CheckoutPageLocator:
    """Locators for elements on the checkout page."""

    CHECKOUT_INFO = (By.CSS_SELECTOR, "[data-qa='checkout-info']")

    DELIVERY_ADDRESS = (By.ID, "address_delivery")
    BILLING_ADDRESS = (By.ID, "address_invoice")

    ADDRESS_NAME = (By.CSS_SELECTOR, ".address_firstname.address_lastname")
    ADDRESS_LINE = (By.CSS_SELECTOR, ".address_address1.address_address2")
    ADDRESS_CITY_STATE_POSTCODE = (
        By.CSS_SELECTOR,
        ".address_city.address_state_name.address_postcode",
    )
    ADDRESS_COUNTRY = (By.CSS_SELECTOR, ".address_country_name")
    ADDRESS_PHONE = (By.CSS_SELECTOR, ".address_phone")

    ORDER_PRODUCT_ROWS = (
        By.CSS_SELECTOR,
        "#cart_info tbody tr[id^='product-']",
    )

    PRODUCT_NAME = (By.CSS_SELECTOR, ".cart_description h4 a")
    PRODUCT_CATEGORY = (By.CSS_SELECTOR, ".cart_description p")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".cart_price p")
    PRODUCT_QUANTITY = (By.CSS_SELECTOR, ".cart_quantity button")
    PRODUCT_TOTAL = (By.CSS_SELECTOR, ".cart_total_price")

    TOTAL_AMOUNT = (
        By.CSS_SELECTOR,
        "#cart_info tbody tr:last-child .cart_total_price",
    )

    ORDER_MESSAGE = (By.NAME, "message")
    PLACE_ORDER = (By.CSS_SELECTOR, "a.check_out")


class CheckoutPageClass(BasePageClass):
    """Page object for the checkout page."""

    CHECKOUT_URL = "https://www.automationexercise.com/checkout"

    def __init__(self, driver) -> None:
        """Initialize the checkout page.

        Args:
            driver: Selenium WebDriver instance.
        """
        super().__init__(driver)

    def get_delivery_address(self) -> dict:
        """Get the delivery address displayed on the checkout page.

        Returns:
            dict: Delivery address details including name, address, city,
                state, postcode, country, and phone number.
        """
        address = self.locate_element(
            CheckoutPageLocator.DELIVERY_ADDRESS
        )

        address_data = self._get_address_details(address)

        logger.info(
            f"Retrieved delivery address: {address_data}"
        )

        return address_data

    def get_billing_address(self) -> dict:
        """Get the billing address displayed on the checkout page.

        Returns:
            dict: Billing address details including name, address, city,
                state, postcode, country, and phone number.
        """
        address = self.locate_element(
            CheckoutPageLocator.BILLING_ADDRESS
        )

        address_data = self._get_address_details(address)

        logger.info(
            f"Retrieved billing address: {address_data}"
        )

        return address_data

    def _get_address_details(self, address_element) -> dict:
        """Extract address details from an address container.

        Args:
            address_element: WebElement containing address information.

        Returns:
            dict: Parsed address information.
        """
        address_lines = address_element.find_elements(
            *CheckoutPageLocator.ADDRESS_LINE
        )

        address_data = {
            "name": address_element.find_element(
                *CheckoutPageLocator.ADDRESS_NAME
            ).text,
            "address_lines": [
                element.text
                for element in address_lines
                if element.text.strip()
            ],
            "city_state_postcode": address_element.find_element(
                *CheckoutPageLocator.ADDRESS_CITY_STATE_POSTCODE
            ).text,
            "country": address_element.find_element(
                *CheckoutPageLocator.ADDRESS_COUNTRY
            ).text,
            "phone": address_element.find_element(
                *CheckoutPageLocator.ADDRESS_PHONE
            ).text,
        }

        return address_data

    def get_order_product_count(self) -> int:
        """Get the number of products listed in the order review.

        Returns:
            int: Number of products in the order.
        """
        products = self.driver.find_elements(
            *CheckoutPageLocator.ORDER_PRODUCT_ROWS
        )

        logger.info(
            f"Number of products in checkout order: {len(products)}"
        )

        return len(products)

    def get_order_total(self) -> int:
        """Get the total amount displayed for the order.

        Returns:
            int: Total order amount without the currency prefix.
        """
        total_element = self.locate_element(
            CheckoutPageLocator.TOTAL_AMOUNT
        )

        total_text = total_element.text

        total_amount = int(
            total_text.replace("Rs. ", "").strip()
        )

        logger.info(
            f"Checkout order total amount: {total_amount}"
        )

        return total_amount

    def enter_order_comment(self, comment: str) -> None:
        """Enter a comment for the order.

        Args:
            comment: Comment to be added to the order.
        """
        logger.info(
            f"Entering order comment: '{comment}'"
        )

        self.enter_text(
            CheckoutPageLocator.ORDER_MESSAGE,
            comment,
        )

    def place_order(self) -> None:
        """Place the order and navigate to the payment page."""
        logger.info("Clicking Place Order.")

        self.click_element(CheckoutPageLocator.PLACE_ORDER)

        self.wait_for_url_contains("/payment")

        logger.info(
            "Successfully navigated to the payment page."
        )

    def is_checkout_page_visible(self) -> bool:
        """
        Verify if the checkout page is opened.
        Returns: bool

        """
        return self.is_element_visible(CheckoutPageLocator.CHECKOUT_INFO)