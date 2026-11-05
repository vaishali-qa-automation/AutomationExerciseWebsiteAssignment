import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePageClass

logger = logging.getLogger(__name__)


class CheckoutModalLocator:
    """Locators for the checkout modal shown to guests who try to check out."""

    MODAL = (By.ID, "checkoutModal")
    TITLE = (By.CSS_SELECTOR, "#checkoutModal .modal-title")
    MESSAGE = (By.CSS_SELECTOR, "#checkoutModal .modal-body p.text-center:first-of-type")
    REGISTER_LOGIN_LINK = (By.CSS_SELECTOR, "#checkoutModal .modal-body a[href='/login']")
    CONTINUE_ON_CART = (By.CSS_SELECTOR, "#checkoutModal .close-checkout-modal")


class CheckoutModalClass(BasePageClass):
    """Page component representing the checkout modal (login/register prompt)."""

    def is_visible(self) -> bool:
        """Check whether the checkout modal is visible.

        Returns:
            bool: True if the modal is visible, otherwise False.
        """
        is_visible = self.is_element_visible(CheckoutModalLocator.MODAL)

        if is_visible:
            logger.info("Checkout modal is visible.")
        else:
            logger.info("Checkout modal is not visible.")

        return is_visible

    def get_title(self) -> str:
        """Get the title displayed in the checkout modal.

        Returns:
            str: Modal title.
        """
        title_element = self.locate_element(CheckoutModalLocator.TITLE)
        return title_element.text

    def get_message(self) -> str:
        """Get the message prompting the user to register or log in.

        Returns:
            str: Modal message text.
        """
        message_element = self.locate_element(CheckoutModalLocator.MESSAGE)
        return message_element.text

    def click_register_login(self) -> None:
        """Navigate to the login/register page from the checkout modal."""
        self.click_element(CheckoutModalLocator.REGISTER_LOGIN_LINK)

        self.wait_for_url_contains("/login")

        logger.info("Navigated to the login page from the checkout modal.")

    def continue_on_cart(self) -> None:
        """Close the modal and stay on the cart page."""
        self.click_element(CheckoutModalLocator.CONTINUE_ON_CART)

        logger.info("Closed the checkout modal and continued on the cart.")