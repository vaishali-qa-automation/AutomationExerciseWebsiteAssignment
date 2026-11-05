import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePageClass

logger = logging.getLogger(__name__)


class PaymentPageLocator:
    """Locators for elements on the payment page."""

    PAYMENT_FORM = (By.ID, "payment-form")

    NAME_ON_CARD = (
        By.CSS_SELECTOR,
        "input[data-qa='name-on-card']",
    )

    CARD_NUMBER = (
        By.CSS_SELECTOR,
        "input[data-qa='card-number']",
    )

    CVC = (
        By.CSS_SELECTOR,
        "input[data-qa='cvc']",
    )

    EXPIRY_MONTH = (
        By.CSS_SELECTOR,
        "input[data-qa='expiry-month']",
    )

    EXPIRY_YEAR = (
        By.CSS_SELECTOR,
        "input[data-qa='expiry-year']",
    )

    PAY_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-qa='pay-button']",
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "#success_message .alert-success",
    )
    ORDER_PLACED = (
        By.CSS_SELECTOR,
        "[data-qa='order-placed']"
    )


class PaymentPageClass(BasePageClass):
    """Page object for the payment page."""

    PAYMENT_URL = "https://www.automationexercise.com/payment"

    def __init__(self, driver) -> None:
        """Initialize the payment page.

        Args:
            driver: Selenium WebDriver instance.
        """
        super().__init__(driver)

    def enter_name_on_card(self, name: str) -> None:
        """Enter the name printed on the payment card.

        Args:
            name: Name to enter in the Name on Card field.
        """
        logger.info(
            f"Entering name on card: '{name}'"
        )

        self.enter_text(
            PaymentPageLocator.NAME_ON_CARD,
            name,
        )

    def enter_card_number(self, card_number: str) -> None:
        """Enter the payment card number.

        Args:
            card_number: Card number to enter.
        """
        logger.info("Entering card number.")

        self.enter_text(
            PaymentPageLocator.CARD_NUMBER,
            card_number,
        )

    def enter_cvc(self, cvc: str) -> None:
        """Enter the card verification code.

        Args:
            cvc: Card verification code.
        """
        logger.info("Entering CVC.")

        self.enter_text(
            PaymentPageLocator.CVC,
            cvc,
        )

    def enter_expiry_month(self, expiry_month: str) -> None:
        """Enter the card expiry month.

        Args:
            expiry_month: Two-digit card expiry month.
        """
        logger.info(
            f"Entering card expiry month: '{expiry_month}'."
        )

        self.enter_text(
            PaymentPageLocator.EXPIRY_MONTH,
            expiry_month,
        )

    def enter_expiry_year(self, expiry_year: str) -> None:
        """Enter the card expiry year.

        Args:
            expiry_year: Four-digit card expiry year.
        """
        logger.info(
            f"Entering card expiry year: '{expiry_year}'."
        )

        self.enter_text(
            PaymentPageLocator.EXPIRY_YEAR,
            expiry_year,
        )

    def enter_card_details(
        self,
        name: str,
        card_number: str,
        cvc: str,
        expiry_month: str,
        expiry_year: str,
    ) -> None:
        """Enter all required payment card details.

        Args:
            name: Name printed on the card.
            card_number: Payment card number.
            cvc: Card verification code.
            expiry_month: Two-digit card expiry month.
            expiry_year: Four-digit card expiry year.
        """
        logger.info("Entering payment card details.")

        self.enter_name_on_card(name)
        self.enter_card_number(card_number)
        self.enter_cvc(cvc)
        self.enter_expiry_month(expiry_month)
        self.enter_expiry_year(expiry_year)

    def pay_and_confirm_order(self) -> None:
        """Submit the payment and confirm the order.

        Raises:
            TimeoutException: If the payment button cannot be clicked.
        """
        logger.info(
            "Clicking Pay and Confirm Order."
        )

        self.click_element(PaymentPageLocator.PAY_BUTTON)

        logger.info(
            "Payment form submitted."
        )

    def is_order_placed_successfully(self) -> bool:
        """Check whether the order was placed successfully.

        Returns:
            bool: True if the success message is visible, otherwise False.
        """
        is_successful = self.is_element_visible(
            PaymentPageLocator.ORDER_PLACED, timeout=10
        )

        if is_successful:
            logger.info(
                "Order placed successfully."
            )
        else:
            logger.warning(
                "Order success message was not displayed."
            )

        return is_successful