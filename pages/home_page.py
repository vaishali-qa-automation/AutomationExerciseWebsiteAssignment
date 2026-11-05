import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePageClass
from pages.components.cart_modal import CartModalClass
from pages.components.header_components import HeaderComponentClass
from pages.components.product_tile import ProductTile

logger = logging.getLogger(__name__)


class HomePageLocator:
    """Locators for elements available on the Automation Exercise homepage."""

    # ------------------------------------------------------------------
    # Carousel
    # ------------------------------------------------------------------

    CAROUSEL = (
        By.ID,
        "slider-carousel",
    )

    CAROUSEL_SLIDES = (
        By.CSS_SELECTOR,
        "#slider-carousel .carousel-inner .item",
    )

    ACTIVE_CAROUSEL_SLIDE = (
        By.CSS_SELECTOR,
        "#slider-carousel .carousel-inner .item.active",
    )

    CAROUSEL_NEXT_BUTTON = (
        By.CSS_SELECTOR,
        "#slider-carousel a.right.control-carousel",
    )

    CAROUSEL_PREVIOUS_BUTTON = (
        By.CSS_SELECTOR,
        "#slider-carousel a.left.control-carousel",
    )

    CAROUSEL_INDICATORS = (
        By.CSS_SELECTOR,
        "#slider-carousel .carousel-indicators li",
    )

    # ------------------------------------------------------------------
    # Category
    # ------------------------------------------------------------------

    CATEGORY_SECTION = (
        By.CSS_SELECTOR,
        ".category-products",
    )

    CATEGORY_WOMEN = (
        By.ID,
        "Women",
    )

    CATEGORY_MEN = (
        By.ID,
        "Men",
    )

    CATEGORY_KIDS = (
        By.ID,
        "Kids",
    )

    # ------------------------------------------------------------------
    # Featured Products
    # ------------------------------------------------------------------

    FEATURED_PRODUCTS_SECTION = (
        By.CSS_SELECTOR,
        ".features_items",
    )

    FEATURED_PRODUCT_TILES = (
        By.CSS_SELECTOR,
        ".features_items .product-image-wrapper",
    )

    # ------------------------------------------------------------------
    # Recommended Products
    # ------------------------------------------------------------------

    RECOMMENDED_PRODUCTS_SECTION = (
        By.CSS_SELECTOR,
        ".recommended_items",
    )

    RECOMMENDED_PRODUCT_TILES = (
        By.CSS_SELECTOR,
        ".recommended_items .product-image-wrapper",
    )

    # ------------------------------------------------------------------
    # Subscription
    # ------------------------------------------------------------------

    SUBSCRIPTION_EMAIL = (
        By.ID,
        "susbscribe_email",
    )

    SUBSCRIPTION_BUTTON = (
        By.ID,
        "subscribe",
    )

    SUBSCRIPTION_SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        ".alert-success.alert",
    )


class HomePageClass(BasePageClass):
    """Page object for the Automation Exercise homepage."""

    HOME_PAGE_URL = "https://www.automationexercise.com/"

    def __init__(self, driver) -> None:
        """Initialize the homepage page object.

        Args:
            driver: Selenium WebDriver instance used to interact with
                the homepage.
        """
        super().__init__(driver)
        self.cart_modal = CartModalClass(driver)
        self.header_component = HeaderComponentClass(driver)

    # ==================================================================
    # Page Navigation
    # ==================================================================

    def navigate_to_home_page(self) -> None:
        """Navigate to the Automation Exercise homepage.

        Navigates directly to the homepage URL and waits until the
        expected URL is loaded.
        """
        logger.info(f"Navigating to homepage: {self.HOME_PAGE_URL}")

        self.navigate_to_url(self.HOME_PAGE_URL)

        logger.info("Successfully navigated to homepage.")

    # ==================================================================
    # Carousel
    # ==================================================================

    def is_carousel_visible(self) -> bool:
        """Check whether the homepage carousel is visible.

        Returns:
            bool: True if the carousel is visible; otherwise False.
        """
        logger.info("Checking whether homepage carousel is visible.")

        return self.is_element_visible(
            HomePageLocator.CAROUSEL
        )

    def get_carousel_slide_count(self) -> int:
        """Return the number of slides available in the carousel.

        Returns:
            int: Number of carousel slides.
        """
        slides = self.driver.find_elements(
            *HomePageLocator.CAROUSEL_SLIDES
        )

        logger.info(f"Found {len(slides)} carousel slides.")

        return len(slides)

    def get_active_carousel_slide_index(self) -> int:
        """Return the zero-based index of the active carousel slide.

        Returns:
            int: Zero-based index of the active carousel slide.

        Raises:
            AssertionError: If no active carousel slide is found.
        """
        slides = self.driver.find_elements(
            *HomePageLocator.CAROUSEL_SLIDES
        )

        for index, slide in enumerate(slides):
            if "active" in slide.get_attribute("class").split():
                logger.info(
                    f"Active carousel slide index is {index}."
                )
                return index

        raise AssertionError(
            "No active carousel slide was found."
        )

    def click_next_carousel_slide(self) -> None:
        """Move the carousel to the next slide."""
        logger.info("Clicking next carousel slide.")

        next_button = self.locate_element(
            HomePageLocator.CAROUSEL_NEXT_BUTTON
        )

        self.click_element(next_button)

        logger.info("Successfully clicked next carousel slide.")

    def click_previous_carousel_slide(self) -> None:
        """Move the carousel to the previous slide."""
        logger.info("Clicking previous carousel slide.")

        previous_button = self.locate_element(
            HomePageLocator.CAROUSEL_PREVIOUS_BUTTON
        )

        self.click_element(previous_button)

        logger.info(
            "Successfully clicked previous carousel slide."
        )

    def get_carousel_indicator_count(self) -> int:
        """Return the number of carousel navigation indicators.

        Returns:
            int: Number of carousel indicators.
        """
        indicators = self.driver.find_elements(
            *HomePageLocator.CAROUSEL_INDICATORS
        )

        logger.info(
            f"Found {len(indicators)} carousel indicators."
        )

        return len(indicators)

    # ==================================================================
    # Categories
    # ==================================================================

    def is_category_section_visible(self) -> bool:
        """Check whether the category section is visible.

        Returns:
            bool: True if the category section is visible; otherwise False.
        """
        return self.is_element_visible(
            HomePageLocator.CATEGORY_SECTION
        )

    def expand_category(self, category: str) -> None:
        """Expand a product category accordion.

        Args:
            category: Category to expand. Supported categories are
                ``Women``, ``Men``, and ``Kids``.

        Raises:
            ValueError: If the provided category is not supported.
        """
        category_locators = {
            "women": HomePageLocator.CATEGORY_WOMEN,
            "men": HomePageLocator.CATEGORY_MEN,
            "kids": HomePageLocator.CATEGORY_KIDS,
        }

        category_key = category.lower()

        if category_key not in category_locators:
            raise ValueError(
                f"Unsupported category '{category}'. "
                f"Supported categories are: "
                f"{', '.join(category_locators.keys())}."
            )

        logger.info(
            f"Expanding product category: {category}"
        )

        category_element = self.locate_element(
            category_locators[category_key]
        )

        self.click_element(category_element)

        logger.info(
            f"Successfully expanded product category: {category}"
        )

    # ==================================================================
    # Featured Products
    # ==================================================================

    def get_featured_product_count(self) -> int:
        """Return the number of featured products displayed.

        Returns:
            int: Number of featured product tiles.
        """
        product_tiles = self.driver.find_elements(
            *HomePageLocator.FEATURED_PRODUCT_TILES
        )

        logger.info(
            f"Found {len(product_tiles)} featured products."
        )

        return len(product_tiles)

    def get_featured_product(
        self,
        product_index: int = 0,
    ) -> ProductTile:
        """Return a featured product as a ProductTile object.

        Args:
            product_index: Zero-based index of the featured product.

        Returns:
            ProductTile: ProductTile instance representing the
                requested product.

        Raises:
            IndexError: If the product index is outside the available
                product range.
        """
        product_tiles = self.driver.find_elements(
            *HomePageLocator.FEATURED_PRODUCT_TILES
        )

        if not 0 <= product_index < len(product_tiles):
            raise IndexError(
                f"Featured product index {product_index} is invalid. "
                f"Available product count: {len(product_tiles)}."
            )

        logger.info(
            f"Getting featured product at index {product_index}."
        )

        return ProductTile(
            product_tiles[product_index]
        )

    def get_featured_product_info(
        self,
        product_index: int = 0,
    ) -> tuple[str, int, int | None]:
        """Return name, price, and ID for a featured product.

        Args:
            product_index: Zero-based index of the featured product.

        Returns:
            tuple[str, int, int | None]: Product name, price, and ID.
        """
        product = self.get_featured_product(product_index)

        product_info = (
            product.name,
            product.price,
            product.id,
        )

        logger.info(
            f"Featured product information: {product_info}"
        )

        return product_info

    def add_featured_product_to_cart(
        self,
        product_index: int = 0,
    ) -> None:
        """Add a featured product to the shopping cart.

        Args:
            product_index: Zero-based index of the featured product.
        """
        product = self.get_featured_product(product_index)

        logger.info(
            f"Adding featured product at index "
            f"{product_index} to cart."
        )
        self.click_element(
            product.add_to_cart_button_elem
        )

        logger.info(
            f"Successfully added featured product at index "
            f"{product_index} to cart."
        )

    def view_featured_product(
        self,
        product_index: int = 0,
    ) -> None:
        """Open the details page of a featured product.

        Args:
            product_index: Zero-based index of the featured product.
        """
        product = self.get_featured_product(product_index)

        logger.info(
            f"Opening featured product at index {product_index}."
        )

        product.view_product_button_elem.click()

        self.wait_for_url_contains(
            "/product_details/"
        )

        logger.info(
            "Successfully navigated to product details page."
        )

    # ==================================================================
    # Recommended Products
    # ==================================================================

    def get_recommended_product_count(self) -> int:
        """Return the number of recommended products displayed.

        Returns:
            int: Number of recommended product tiles.
        """
        product_tiles = self.driver.find_elements(
            *HomePageLocator.RECOMMENDED_PRODUCT_TILES
        )

        logger.info(
            f"Found {len(product_tiles)} recommended products."
        )

        return len(product_tiles)

    def get_recommended_product(
        self,
        product_index: int = 0,
    ) -> ProductTile:
        """Return a recommended product as a ProductTile object.

        Args:
            product_index: Zero-based index of the recommended product.

        Returns:
            ProductTile: ProductTile instance representing the
                requested product.

        Raises:
            IndexError: If the product index is outside the available
                product range.
        """
        product_tiles = self.driver.find_elements(
            *HomePageLocator.RECOMMENDED_PRODUCT_TILES
        )

        if not 0 <= product_index < len(product_tiles):
            raise IndexError(
                f"Recommended product index {product_index} is invalid. "
                f"Available product count: {len(product_tiles)}."
            )

        logger.info(
            f"Getting recommended product at index {product_index}."
        )

        return ProductTile(
            product_tiles[product_index]
        )

    def add_recommended_product_to_cart(
        self,
        product_index: int = 0,
    ) -> None:
        """Add a recommended product to the shopping cart.

        Args:
            product_index: Zero-based index of the recommended product.
        """
        product = self.get_recommended_product(product_index)

        logger.info(
            f"Adding recommended product at index "
            f"{product_index} to cart."
        )

        product.add_to_cart_button_elem.click()

        logger.info(
            f"Successfully added recommended product at index "
            f"{product_index} to cart."
        )

    # ==================================================================
    # Subscription
    # ==================================================================

    def subscribe_to_newsletter(
        self,
        email_address: str,
    ) -> None:
        """Subscribe an email address to the homepage newsletter.

        Args:
            email_address: Email address to use for the subscription.
        """
        logger.info(
            f"Subscribing email address '{email_address}'."
        )

        self.enter_text(
            HomePageLocator.SUBSCRIPTION_EMAIL,
            email_address,
        )

        self.click_element(HomePageLocator.SUBSCRIPTION_BUTTON)

        logger.info(
            f"Successfully submitted newsletter subscription "
            f"for '{email_address}'."
        )

    def is_subscription_success_message_visible(self) -> bool:
        """Check whether the subscription success message is visible.

        Returns:
            bool: True if the success message is visible; otherwise False.
        """
        return self.is_element_visible(
            HomePageLocator.SUBSCRIPTION_SUCCESS_MESSAGE
        )