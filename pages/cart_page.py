import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePageClass
from pages.components.headers_components import HeaderComponentClass

logger = logging.getLogger(__name__)


class CartPageLocator:
    """Locators for elements on the shopping cart page."""

    CART_INFO_TABLE = (By.ID, "cart_info_table")
    CART_PRODUCT_ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr[id^='product-']")
    PROCEED_TO_CHECKOUT = (By.CSS_SELECTOR, "a.check_out")

    CHECKOUT_MODAL = (
        By.ID,
        "checkoutModal"
    )

    CHECKOUT_MODAL_TITLE = (
        By.CSS_SELECTOR,
        "#checkoutModal .modal-title"
    )

    CHECKOUT_MODAL_MESSAGE = (
        By.CSS_SELECTOR,
        "#checkoutModal .modal-body p.text-center:first-child"
    )

    LOGIN_REGISTER_LINK_FROM_MODAL = (
        By.CSS_SELECTOR,
        "#checkoutModal a[href='/login']"
    )

    CONTINUE_ON_CART_BUTTON = (
        By.CSS_SELECTOR,
        "#checkoutModal .close-checkout-modal"
    )

    EMPTY_CART = (By.ID, "empty_cart")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".cart_description h4 a")
    PRODUCT_CATEGORY = (By.CSS_SELECTOR, ".cart_description p")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".cart_price p")
    PRODUCT_QUANTITY = (By.CSS_SELECTOR, ".cart_quantity button")
    PRODUCT_TOTAL = (By.CSS_SELECTOR, ".cart_total_price")
    PRODUCT_DELETE = (By.CSS_SELECTOR, ".cart_quantity_delete")


class CartProduct:
    """Represents a single product row in the shopping cart."""

    def __init__(self, product_element: WebElement) -> None:
        """Initialize a cart product component.

        Args:
            product_element: WebElement representing a product row in the cart.
        """
        self.product_element = product_element

    @property
    def name(self) -> str:
        """Get the product name.

        Returns:
            str: Product name displayed in the cart.
        """
        return self.product_element.find_element(
            *CartPageLocator.PRODUCT_NAME
        ).text

    @property
    def category(self) -> str:
        """Get the product category.

        Returns:
            str: Product category displayed in the cart.
        """
        return self.product_element.find_element(
            *CartPageLocator.PRODUCT_CATEGORY
        ).text

    @property
    def price(self) -> int:
        """Get the unit price of the product.

        Returns:
            int: Product price without the currency prefix.
        """
        price_text = self.product_element.find_element(
            *CartPageLocator.PRODUCT_PRICE
        ).text

        return int(price_text.replace("Rs. ", "").strip())

    @property
    def quantity(self) -> int:
        """Get the quantity of the product.

        Returns:
            int: Number of units of the product in the cart.
        """
        quantity_text = self.product_element.find_element(
            *CartPageLocator.PRODUCT_QUANTITY
        ).text

        return int(quantity_text)

    @property
    def total(self) -> int:
        """Get the total price for the product.

        Returns:
            int: Total product price without the currency prefix.
        """
        total_text = self.product_element.find_element(
            *CartPageLocator.PRODUCT_TOTAL
        ).text

        return int(total_text.replace("Rs. ", "").strip())

    @property
    def product_id(self) -> int | None:
        """Get the product ID from the cart row.

        Returns:
            int | None: Product ID if available, otherwise None.
        """
        product_id = self.product_element.get_attribute("id")

        if product_id and product_id.startswith("product-"):
            return int(product_id.replace("product-", ""))

        return None

    @property
    def delete_button(self) -> WebElement:
        """Get the delete button for the product.

        Returns:
            WebElement: Product delete button.
        """
        return self.product_element.find_element(
            *CartPageLocator.PRODUCT_DELETE
        )


class CartPageClass(BasePageClass):
    """Page object for the shopping cart page."""

    CART_URL = "https://www.automationexercise.com/view_cart"

    def __init__(self, driver) -> None:
        """Initialize the cart page.

        Args:
            driver: Selenium WebDriver instance.
        """
        super().__init__(driver)
        self.header_component = HeaderComponentClass(driver)

    def get_product_count(self) -> int:
        """Get the number of products currently present in the cart.

        Returns:
            int: Number of product rows in the cart.
        """
        products = self.driver.find_elements(
            *CartPageLocator.CART_PRODUCT_ROWS
        )

        logger.info(f"Number of products in cart: {len(products)}")

        return len(products)

    def get_product(self, product_index: int = 0) -> CartProduct:
        """Get a cart product by its index.

        Args:
            product_index: Zero-based index of the product.

        Returns:
            CartProduct: Cart product component.

        Raises:
            IndexError: If the product index is outside the available range.
        """
        products = self.driver.find_elements(
            *CartPageLocator.CART_PRODUCT_ROWS
        )

        if product_index >= len(products):
            raise IndexError(
                f"Product index {product_index} is out of range. "
                f"Cart contains {len(products)} product(s)."
            )

        logger.info(f"Getting product at cart index {product_index}")

        return CartProduct(products[product_index])

    def get_product_info(self, product_index: int = 0) -> dict:
        """Get information about a product in the cart.

        Args:
            product_index: Zero-based index of the product.

        Returns:
            dict: Product name, category, price, quantity, and total.
        """
        product = self.get_product(product_index)

        product_info = {
            "id": product.product_id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "quantity": product.quantity,
            "total": product.total,
        }

        logger.info(
            f"Retrieved cart product information: {product_info}"
        )

        return product_info

    def remove_product(self, product_index: int = 0) -> None:
        """Remove a product from the shopping cart.

        Args:
            product_index: Zero-based index of the product to remove.

        Raises:
            IndexError: If the product index is outside the available range.
        """
        product = self.get_product(product_index)

        logger.info(
            f"Removing product '{product.name}' "
            f"with ID '{product.product_id}' from cart."
        )

        product.delete_button.click()

    def proceed_to_checkout(self) -> None:
        """Proceed from the cart to the checkout page.

        If the user is not logged in, the website displays a checkout
        modal instead of navigating to checkout.

        Raises:
            TimeoutException: If the checkout button cannot be located
                or clicked.
        """
        logger.info("Attempting to proceed to checkout.")

        self.click_element(
            CartPageLocator.PROCEED_TO_CHECKOUT
        )

    def is_cart_empty(self) -> bool:
        """Check whether the shopping cart is empty.

        The cart is considered empty when the empty-cart message is
        displayed on the page.

        Returns:
            bool: True if the cart is empty, otherwise False.
        """
        is_empty = self.is_element_visible(
            CartPageLocator.EMPTY_CART
        )

        if is_empty:
            logger.info("Shopping cart is empty.")
        else:
            logger.info("Shopping cart contains one or more products.")

        return is_empty