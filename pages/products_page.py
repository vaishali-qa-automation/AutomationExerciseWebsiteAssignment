import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePageClass
from pages.components.cart_modal import CartModalClass
from pages.components.headers_components import HeaderComponentClass
from pages.components.product_tile import ProductTile

logger = logging.getLogger(__name__)


class ProductsLocator:
    """Locators for the products listing page."""

    SEARCH_BOX = (By.ID, "search_product")
    SEARCH_CONFIRM = (By.ID, "submit_search")

    CATEGORY = (By.CLASS_NAME, "category-products")
    CATEGORY_WOMEN = (By.ID, "Women")
    CATEGORY_MEN = (By.ID, "Men")
    CATEGORY_KIDS = (By.ID, "Kids")

    BRAND = (By.CLASS_NAME, "brands_products")
    BRANDS_NAME_CONTAINER = (By.CSS_SELECTOR, ".brands-name li")

    SINGLE_PRODUCT_TILE = (By.CLASS_NAME, "product-image-wrapper")

    CART_MODAL = (By.ID, "cartModal")
    CART_MODAL_TITLE = (By.CSS_SELECTOR, "#cartModal .modal-title")
    CART_MODAL_MESSAGE = (By.CSS_SELECTOR, "#cartModal .modal-body p")
    CART_MODAL_VIEW_CART = (
        By.CSS_SELECTOR,
        "#cartModal a[href='/view_cart']",
    )
    CART_MODAL_CONTINUE_SHOPPING = (
        By.CSS_SELECTOR,
        "#cartModal .close-modal",
    )

    @classmethod
    def brands_name(cls, brand_name: str) -> tuple[str, str]:
        """Create a locator for a specific product brand.

        Args:
            brand_name: Name of the product brand.

        Returns:
            Selenium locator tuple for the requested brand.
        """
        return (
            By.CSS_SELECTOR,
            (f"{cls.BRANDS_NAME_CONTAINER[1]} "
            f"a[href*='/brand_products/{brand_name}']"),
        )


class ProductViewLocator:
    """Locators for the individual product details page."""

    PRODUCT_DETAILS = (By.CLASS_NAME, "product-details")

    PRODUCT_IMAGE = (
        By.CSS_SELECTOR,
        ".product-details .view-product img",
    )

    PRODUCT_INFORMATION = (
        By.CLASS_NAME,
        "product-information",
    )

    PRODUCT_NAME = (
        By.CSS_SELECTOR,
        ".product-information h2",
    )

    PRODUCT_CATEGORY = (
        By.CSS_SELECTOR,
        ".product-information p",
    )

    PRODUCT_PRICE = (
        By.CSS_SELECTOR,
        ".product-information span span",
    )

    QUANTITY = (By.ID, "quantity")

    PRODUCT_ID = (By.ID, "product_id")

    ADD_TO_CART = (
        By.CSS_SELECTOR,
        ".product-information button.cart",
    )

    AVAILABILITY = (
        By.XPATH,
        "//div[@class='product-information']//b[normalize-space()='Availability:']/parent::p",
    )

    CONDITION = (
        By.XPATH,
        "//div[@class='product-information']//b[normalize-space()='Condition:']/parent::p",
    )

    BRAND = (
        By.XPATH,
        "//div[@class='product-information']//b[normalize-space()='Brand:']/parent::p",
    )

    REVIEW_NAME = (By.ID, "name")
    REVIEW_EMAIL = (By.ID, "email")
    REVIEW_TEXT = (By.ID, "review")
    REVIEW_SUBMIT = (By.ID, "button-review")
    REVIEW_SUCCESS = (By.CSS_SELECTOR, "#review-section .alert-success")


class ProductsClass(BasePageClass):
    """Page object for the products listing page."""

    def __init__(self, driver) -> None:
        """Initialize the products page.

        Args:
            driver: Selenium WebDriver instance used to interact with
                the products page.
        """
        super().__init__(driver)
        self.cart_modal = CartModalClass(driver)
        self.header_component = HeaderComponentClass(driver)

    def search_product(self, product_name: str) -> None:
        """Search for a product using the product search field.

        Args:
            product_name: Product name or search text to enter.
        """
        logger.info("Searching for product: %s", product_name)

        self.enter_text(
            ProductsLocator.SEARCH_BOX,
            product_name,
        )
        self.click_element(
            ProductsLocator.SEARCH_CONFIRM
        )

        logger.info(
            "Product search submitted for: %s",
            product_name,
        )

    def click_on_product_category(
        self,
        category_type: str,
        product_category: str,
    ) -> None:
        """Select a specific product category.

        Args:
            category_type: Parent category such as ``Women``, ``Men``,
                or ``Kids``.
            product_category: Specific category to select under the
                parent category.

        Raises:
            ValueError: If the supplied category type is not supported.
        """
        category_locators = {
            "women": ProductsLocator.CATEGORY_WOMEN,
            "men": ProductsLocator.CATEGORY_MEN,
            "kids": ProductsLocator.CATEGORY_KIDS,
        }

        category_key = category_type.lower()

        if category_key not in category_locators:
            logger.error(
                "Unsupported product category type: %s",
                category_type,
            )
            raise ValueError(
                f"Unsupported category type: {category_type}"
            )

        category_element = self.locate_element(
            category_locators[category_key]
        )

        specific_category = category_element.find_element(
            By.PARTIAL_LINK_TEXT,
            product_category,
        )

        self.wait_for_element_to_be_clickable(
            specific_category
        )
        specific_category.click()

        logger.info(
            f"Selected product category:{category_type} > {product_category}"
        )

    def click_on_brand(self, brand_name: str) -> None:
        """Filter products by brand.

        Args:
            brand_name: Name of the brand to select.

        Raises:
            ValueError: If the brand name is empty.
        """
        if not brand_name:
            raise ValueError("Brand name cannot be empty.")

        logger.info(f"Selecting product brand: {brand_name}")

        brand_locator = ProductsLocator.brands_name(brand_name)

        self.click_element(brand_locator)

        self.wait_for_url_contains(
            f"/brand_products/{brand_name.capitalize()}"
        )

        logger.info(
            f"Successfully navigated to brand: {brand_name}"
        )

    def get_current_product_tile_count(self) -> int:
        """Return the number of product tiles currently displayed.

        Returns:
            Number of product tiles present on the page.
        """
        product_tiles = self.driver.find_elements(
            *ProductsLocator.SINGLE_PRODUCT_TILE
        )

        return len(product_tiles)

    def get_product_tile(self, product_tile_index: int = 0) -> "ProductTile":
        """Return a ProductTile object for the requested product.

        Args:
            product_tile_index: Zero-based index of the product tile.

        Returns:
            ProductTile object representing the selected product.

        Raises:
            IndexError: If the requested product index does not exist.
        """
        product_tiles = self.driver.find_elements(
            *ProductsLocator.SINGLE_PRODUCT_TILE
        )

        if not 0 <= product_tile_index < len(product_tiles):
            raise IndexError(
                f"Product tile index {product_tile_index} is out of range. "
                f"Available products: {len(product_tiles)}."
            )

        return ProductTile(product_tiles[product_tile_index])

    def get_product_info(
        self,
        product_tile_index: int = 0,
    ) -> tuple[str, int, int | None]:
        """Get product information from a product tile.

        Args:
            product_tile_index: Zero-based index of the product tile.

        Returns:
            Tuple containing product name, price, and product ID.
        """
        product = self.get_product_tile(product_tile_index)

        return (
            product.name,
            product.price,
            product.id,
        )

    def add_product_to_cart(
        self,
        product_tile_index: int = 0,
    ) -> None:
        """Add a product from the product tile to the shopping cart.

        Args:
            product_tile_index: Zero-based index of the product tile.
        """
        product = self.get_product_tile(product_tile_index)

        logger.info(
            f"Adding product '{product.name}' to cart."
        )

        self.wait_for_element_to_be_clickable(
            product.add_to_cart_button_elem
        )
        product.add_to_cart_button_elem.click()

    def view_product(
        self,
        product_tile_index: int = 0,
    ) -> "ProductViewPage":
        """Open the details page for a product.

        Args:
            product_tile_index: Zero-based index of the product tile.

        Returns:
            ProductViewPage representing the opened product details page.
        """
        product = self.get_product_tile(product_tile_index)

        logger.info(
            f"Opening product details for {product.name}."

        )

        self.wait_for_element_to_be_clickable(
            product.view_product_button_elem
        )
        product.view_product_button_elem.click()

        self.wait_for_url_contains("/product_details/")

        return ProductViewPage(self.driver)

    def is_cart_modal_displayed(self) -> bool:
        """Check whether the add-to-cart confirmation modal is displayed.

        Returns:
            True if the cart confirmation modal is visible, otherwise False.
        """
        return self.locate_element(
            ProductsLocator.CART_MODAL
        ).is_displayed()

    def click_view_cart_from_modal(self) -> None:
        """Open the shopping cart from the add-to-cart confirmation modal."""
        self.click_element(
            ProductsLocator.CART_MODAL_VIEW_CART
        )

        self.wait_for_url_contains("/view_cart")

    def continue_shopping_from_modal(self) -> None:
        """Close the cart confirmation modal and continue shopping."""
        self.click_element(
            ProductsLocator.CART_MODAL_CONTINUE_SHOPPING
        )


class ProductViewPage(BasePageClass):
        """Page object for an individual product details page."""

        def __init__(self, driver) -> None:
            """Initialize the product details page.

            Args:
                driver: Selenium WebDriver instance used to interact with
                    the product details page.
            """
            super().__init__(driver)

        @property
        def name(self) -> str:
            """Return the product name.

            Returns:
                Name of the currently displayed product.
            """
            return self.locate_element(
                ProductViewLocator.PRODUCT_NAME
            ).text.strip()

        @property
        def price(self) -> int:
            """Return the product price.

            Returns:
                Product price as an integer.
            """
            price_element = self.locate_element(
                ProductViewLocator.PRODUCT_PRICE
            )

            return int(
                price_element.text.replace("Rs.", "").strip()
            )

        @property
        def product_id(self) -> int:
            """Return the ID of the currently displayed product.

            Returns:
                Product ID as an integer.
            """
            product_id_element = self.locate_element(
                ProductViewLocator.PRODUCT_ID
            )
            product_id = product_id_element.get_attribute("value")
            if product_id:
                return int(product_id)
            else:
                return None

        @property
        def category(self) -> str:
            """Return the product category text.

            Returns:
                Category information displayed for the product.
            """
            category_element = self.locate_element(
                ProductViewLocator.PRODUCT_CATEGORY
            )

            return category_element.text.strip()

        @property
        def availability(self) -> str:
            """Return the product availability information.

            Returns:
                Availability information such as ``In Stock``.
            """
            return self.locate_element(
                ProductViewLocator.AVAILABILITY
            ).text.strip()

        @property
        def condition(self) -> str:
            """Return the product condition.

            Returns:
                Product condition such as ``New``.
            """
            return self.locate_element(
                ProductViewLocator.CONDITION
            ).text.strip()

        @property
        def brand(self) -> str:
            """Return the product brand.

            Returns:
                Product brand name.
            """
            return self.locate_element(
                ProductViewLocator.BRAND
            ).text.strip()

        def set_quantity(self, quantity: int) -> None:
            """Set the quantity for the product.

            Args:
                quantity: Number of product units to add to the cart.

            Raises:
                ValueError: If quantity is less than one.
            """
            if quantity < 1:
                raise ValueError("Product quantity must be at least 1.")

            quantity_element = self.locate_element(
                ProductViewLocator.QUANTITY
            )

            quantity_element.clear()
            quantity_element.send_keys(str(quantity))

        def add_to_cart(self) -> None:
            """Add the currently displayed product to the shopping cart."""
            logger.info(
                "Adding product '%s' to cart from product details page.",
                self.name,
            )

            self.click_element(
                ProductViewLocator.ADD_TO_CART
            )

        def write_review(
                self,
                name: str,
                email: str,
                review: str,
        ) -> None:
            """Submit a review for the current product.

            Args:
                name: Name of the reviewer.
                email: Email address of the reviewer.
                review: Review text to submit.
            """
            self.enter_text(
                ProductViewLocator.REVIEW_NAME,
                name,
            )

            self.enter_text(
                ProductViewLocator.REVIEW_EMAIL,
                email,
            )

            self.enter_text(
                ProductViewLocator.REVIEW_TEXT,
                review,
            )

            self.click_element(
                ProductViewLocator.REVIEW_SUBMIT
            )

        def is_review_submitted(self) -> bool:
            """Check whether the review submission was successful.

            Returns:
                True if the review success message is displayed.
            """
            return self.locate_element(
                ProductViewLocator.REVIEW_SUCCESS
            ).is_displayed()