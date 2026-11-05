from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ProductTile:
    """Representation of a single product tile on the products page."""

    def __init__(self, product_tile_element: WebElement) -> None:
        """Initialize a product tile.

        Args:
            product_tile_element: WebElement representing the product tile.
        """
        self.product_tile_element = product_tile_element

    @property
    def view_product_button_elem(self) -> WebElement:
        """Return the View Product button element.

        Returns:
            WebElement representing the View Product link.
        """
        return self.product_tile_element.find_element(
            By.CLASS_NAME,
            "choose",
        )

    @property
    def add_to_cart_button_elem(self) -> WebElement:
        """Return the Add to Cart button element.

        Returns:
            WebElement representing the Add to Cart button.
        """
        return self.product_tile_element.find_element(
            By.CSS_SELECTOR,
            ".add-to-cart",
        )

    @property
    def price(self) -> int:
        """Return the product price.

        Returns:
            Product price as an integer.
        """
        price_element = self.product_tile_element.find_element(
            By.CSS_SELECTOR,
            ".productinfo h2",
        )

        return int(
            price_element.text.replace("Rs.", "").strip()
        )

    @property
    def name(self) -> str:
        """Return the product name.

        Returns:
            Product name displayed on the product tile.
        """
        name_element = self.product_tile_element.find_element(
            By.CSS_SELECTOR,
            ".productinfo p",
        )

        return name_element.text.strip()

    @property
    def id(self) -> int | None:
        """Return the product ID.

        Returns:
            Product ID as an integer, or None if the ID is unavailable.
        """
        product_id_element = self.product_tile_element.find_element(
            By.CSS_SELECTOR,
            ".productinfo a",
        )

        product_id = product_id_element.get_attribute(
            "data-product-id"
        )

        return int(product_id) if product_id else None