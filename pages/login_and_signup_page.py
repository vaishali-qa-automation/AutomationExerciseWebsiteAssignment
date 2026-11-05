import logging

from selenium.webdriver.common.by import By

from models.user import User
from pages.base_page import BasePageClass
from pages.components.headers_components import HeaderComponentClass

logger = logging.getLogger(__name__)


class LoginAndSignUpLocators:
    """Locators for login, signup, and account information forms."""

    # Login form
    LOGIN_FORM = (By.CLASS_NAME, "login-form")
    LOGIN_EMAIL_ADDRESS = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")

    # Initial signup form
    SIGNUP_FORM = (By.CLASS_NAME, "signup-form")
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")

    # Account information
    TITLE_MR = (By.ID, "id_gender1")
    TITLE_MRS = (By.ID, "id_gender2")
    ACCOUNT_PASSWORD = (By.ID, "password")

    DATE_OF_BIRTH_DAY = (By.ID, "days")
    DATE_OF_BIRTH_MONTH = (By.ID, "months")
    DATE_OF_BIRTH_YEAR = (By.ID, "years")

    NEWSLETTER_CHECKBOX = (By.ID, "newsletter")
    SPECIAL_OFFERS_CHECKBOX = (By.ID, "optin")

    # Address information
    FIRST_NAME = (By.ID, "first_name")
    LAST_NAME = (By.ID, "last_name")
    COMPANY = (By.ID, "company")
    ADDRESS_1 = (By.ID, "address1")
    ADDRESS_2 = (By.ID, "address2")
    COUNTRY = (By.ID, "country")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    ZIPCODE = (By.ID, "zipcode")
    MOBILE_NUMBER = (By.ID, "mobile_number")

    CREATE_ACCOUNT_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-qa='create-account']",
    )

    ACCOUNT_CREATED_INFO = (By.CSS_SELECTOR, "h2[data-qa='account-created']")


class LoginAndSignUpPageClass(BasePageClass):
    """Page object for login and signup functionality."""

    def __init__(self, driver) -> None:
        """Initialize the login and signup page.

        Args:
            driver: Selenium WebDriver instance used to interact with
                the application.
        """
        super().__init__(driver)
        self.header_component = HeaderComponentClass(driver)

    # ------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------

    def _enter_username(self, username: str) -> None:
        """Enter the username or email address in the login form.

        Args:
            username: Username or email address used for authentication.
        """
        logger.info("Entering login username")
        self.enter_text(
            LoginAndSignUpLocators.LOGIN_EMAIL_ADDRESS,
            username,
        )

    def _enter_password(self, password: str) -> None:
        """Enter the password in the login form.

        Args:
            password: Password used for authentication.
        """
        self.enter_text(
            LoginAndSignUpLocators.LOGIN_PASSWORD,
            password,
        )

    def _click_login_button(self) -> None:
        """Click the login button."""
        self.click_element(LoginAndSignUpLocators.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Log in to the application.

        Args:
            username: Username or email address used for authentication.
            password: Password used for authentication.
        """
        self.header_component.navigate_to_login_page()
        self._enter_username(username)
        self._enter_password(password)
        self._click_login_button()

    # ------------------------------------------------------------------
    # Initial signup
    # ------------------------------------------------------------------

    def _enter_sign_up_name(self, name: str) -> None:
        """Enter the user's name in the signup form.

        Args:
            name: Name to be used for the new account.
        """
        self.enter_text(
            LoginAndSignUpLocators.SIGNUP_NAME,
            name,
        )

    def _enter_sign_up_email(self, email_address: str) -> None:
        """Enter the user's email address in the signup form.

        Args:
            email_address: Email address to be used for the new account.
        """
        self.enter_text(
            LoginAndSignUpLocators.SIGNUP_EMAIL,
            email_address,
        )

    def _click_signup_button(self) -> None:
        """Click the signup button."""
        self.click_element(LoginAndSignUpLocators.SIGNUP_BUTTON)

    def enter_signup_details(
        self,
        name: str,
        email_address: str,
    ) -> None:
        """Submit the initial signup form.

        Args:
            name: Name to be used for the new account.
            email_address: Email address to be used for the new account.
        """
        self.header_component.navigate_to_login_page()
        self._enter_sign_up_name(name)
        self._enter_sign_up_email(email_address)
        self._click_signup_button()

    # ------------------------------------------------------------------
    # Account information
    # ------------------------------------------------------------------

    def _select_title(self, title: str) -> None:
        """Select the title for the new account.

        Args:
            title: Title to select. Supported values are ``Mr`` and ``Mrs``.

        Raises:
            ValueError: If the provided title is not supported.
        """
        title_locators = {
            "Mr": LoginAndSignUpLocators.TITLE_MR,
            "Mrs": LoginAndSignUpLocators.TITLE_MRS,
        }

        if title not in title_locators:
            raise ValueError("Title must be either 'Mr' or 'Mrs'.")
        self.click_element(title_locators[title])

    def _enter_account_password(self, password: str) -> None:
        """Enter the password for the new account.

        Args:
            password: Password to be used for the new account.
        """
        self.enter_text(
            LoginAndSignUpLocators.ACCOUNT_PASSWORD,
            password,
        )

    def _select_date_of_birth(
        self,
        day: str,
        month: str,
        year: str,
    ) -> None:
        """Select the user's date of birth.

        Args:
            day: Day of birth as displayed in the dropdown.
            month: Month of birth as displayed in the dropdown.
            year: Year of birth as displayed in the dropdown.
        """
        self.select_option(
            LoginAndSignUpLocators.DATE_OF_BIRTH_DAY,
            day,
        )
        self.select_option(
            LoginAndSignUpLocators.DATE_OF_BIRTH_MONTH,
            month,
        )
        self.select_option(
            LoginAndSignUpLocators.DATE_OF_BIRTH_YEAR,
            year,
        )

    def _select_checkbox(
        self,
        locator: tuple[str, str],
        should_select: bool,
    ) -> None:
        """Select or deselect a checkbox.

        Args:
            locator: Selenium locator tuple for the checkbox.
            should_select: Whether the checkbox should be selected.
        """
        checkbox = self.locate_element(locator)
        self.wait_for_element_to_be_clickable(checkbox)

        if checkbox.is_selected() != should_select:
            checkbox.click()

    def _select_newsletter(self, subscribe: bool = True) -> None:
        """Select or deselect the newsletter subscription checkbox.

        Args:
            subscribe: Whether the user should subscribe to the newsletter.
        """
        self._select_checkbox(
            LoginAndSignUpLocators.NEWSLETTER_CHECKBOX,
            subscribe,
        )

    def _select_special_offers(self, subscribe: bool = True) -> None:
        """Select or deselect the special-offers checkbox.

        Args:
            subscribe: Whether the user should receive special offers.
        """
        self._select_checkbox(
            LoginAndSignUpLocators.SPECIAL_OFFERS_CHECKBOX,
            subscribe,
        )

    # ------------------------------------------------------------------
    # Address information
    # ------------------------------------------------------------------

    def _enter_first_name(self, first_name: str) -> None:
        """Enter the first name.

        Args:
            first_name: First name of the account holder.
        """
        self.enter_text(
            LoginAndSignUpLocators.FIRST_NAME,
            first_name,
        )

    def _enter_last_name(self, last_name: str) -> None:
        """Enter the last name.

        Args:
            last_name: Last name of the account holder.
        """
        self.enter_text(
            LoginAndSignUpLocators.LAST_NAME,
            last_name,
        )

    def _enter_company(self, company: str) -> None:
        """Enter the company name.

        Args:
            company: Company name associated with the account.
        """
        self.enter_text(
            LoginAndSignUpLocators.COMPANY,
            company,
        )

    def _enter_address(self, address: str) -> None:
        """Enter the primary address.

        Args:
            address: Primary street or postal address.
        """
        self.enter_text(
            LoginAndSignUpLocators.ADDRESS_1,
            address,
        )

    def _enter_address_2(self, address_2: str) -> None:
        """Enter the secondary address.

        Args:
            address_2: Additional address information.
        """
        self.enter_text(
            LoginAndSignUpLocators.ADDRESS_2,
            address_2,
        )

    def _select_country(self, country: str) -> None:
        """Select the country from the country dropdown.

        Args:
            country: Country to select.
        """
        self.select_option(
            LoginAndSignUpLocators.COUNTRY,
            country,
        )

    def _enter_state(self, state: str) -> None:
        """Enter the state or province.

        Args:
            state: State or province of the address.
        """
        self.enter_text(
            LoginAndSignUpLocators.STATE,
            state,
        )

    def _enter_city(self, city: str) -> None:
        """Enter the city.

        Args:
            city: City of the address.
        """
        self.enter_text(
            LoginAndSignUpLocators.CITY,
            city,
        )

    def _enter_zipcode(self, zipcode: str) -> None:
        """Enter the postal or ZIP code.

        Args:
            zipcode: Postal or ZIP code of the address.
        """
        self.enter_text(
            LoginAndSignUpLocators.ZIPCODE,
            zipcode,
        )

    def _enter_mobile_number(self, mobile_number: str) -> None:
        """Enter the mobile phone number.

        Args:
            mobile_number: Mobile phone number associated with the account.
        """
        self.enter_text(
            LoginAndSignUpLocators.MOBILE_NUMBER,
            mobile_number,
        )

    def _click_create_account_button(self) -> None:
        """Click the Create Account button."""
        self.click_element(LoginAndSignUpLocators.CREATE_ACCOUNT_BUTTON)

    # ------------------------------------------------------------------
    # Complete account information
    # ------------------------------------------------------------------

    def enter_account_information(self, user: User) -> None:
        """Enter the account and address information from a User model."""
        address = user.address
        dob = user.date_of_birth

        self._select_title(user.title)
        self._enter_account_password(user.password)
        self._select_date_of_birth(day=dob.day, month=dob.month, year=dob.year)
        self._select_newsletter(user.subscribe_newsletter)
        self._select_special_offers(user.receive_special_offers)

        self._enter_first_name(address.first_name)
        self._enter_last_name(address.last_name)
        self._enter_company(address.company)
        self._enter_address(address.address)
        self._enter_address_2(address.address_2)

        self._select_country(address.country)
        self._enter_state(address.state)
        self._enter_city(address.city)
        self._enter_zipcode(address.zipcode)
        self._enter_mobile_number(address.mobile_number)

    def create_account(self) -> None:
        """Submit the completed account information form."""
        self._click_create_account_button()

    def is_account_created(self) -> bool:
        """
        This method checks if the account has been created.
        Returns: True or False.

        """
        self.locate_element(LoginAndSignUpLocators.ACCOUNT_CREATED_INFO)
        is_created = self.is_element_visible(
            LoginAndSignUpLocators.ACCOUNT_CREATED_INFO
        )
        return is_created
