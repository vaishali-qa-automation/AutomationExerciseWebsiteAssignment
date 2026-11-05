import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePageClass

logger = logging.getLogger(__name__)


class CartModalLocator:
    """Locators for the add-to-cart confirmation modal."""

    MODAL = (By.ID, "cartModal")
    TITLE = (By.CSS_SELECTOR, "#cartModal .modal-title")
    MESSAGE = (By.CSS_SELECTOR, "#cartModal .modal-body p.text-center:first-child")
    VIEW_CART = (By.CSS_SELECTOR, "#cartModal a[href='/view_cart']")
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, "#cartModal .close-modal")


class CartModalClass(BasePageClass):
    """Page component representing the add-to-cart confirmation modal."""

    def is_visible(self) -> bool:
        """Check whether the cart confirmation modal is visible.

        Returns:
            bool: True if the modal is visible, otherwise False.
        """
        is_visible = self.is_element_visible(CartModalLocator.MODAL)

        if is_visible:
            logger.info("Cart confirmation modal is visible.")
        else:
            logger.info("Cart confirmation modal is not visible.")

        return is_visible

    def get_title(self) -> str:
        """Get the title displayed in the cart confirmation modal.

        Returns:
            str: Modal title.
        """
        title_element = self.locate_element(CartModalLocator.TITLE)
        return title_element.text

    def get_message(self) -> str:
        """Get the confirmation message displayed in the modal.

        Returns:
            str: Modal confirmation message.
        """
        message_element = self.locate_element(CartModalLocator.MESSAGE)
        return message_element.text

    def click_view_cart(self) -> None:
        """Navigate to the shopping cart from the confirmation modal."""
        self.click_element(CartModalLocator.VIEW_CART)

        self.wait_for_url_contains("/view_cart")

        logger.info("Navigated to the cart from the confirmation modal.")

    def continue_shopping(self) -> None:
        """
        Close the modal and continue shopping.
        Returns: None

        """
        self.click_element(CartModalLocator.CONTINUE_SHOPPING)

        logger.info("Closed the cart confirmation modal.")