import logging

import pytest

from pages.home_page import HomePageClass
from pages.login_and_signup_page import LoginAndSignUpPageClass

logger = logging.getLogger(__name__)


BASE_URL = "https://www.automationexercise.com/"



@pytest.mark.ui
class TestLoginAndSignup:
    """Signup and login flow tests for automationexercise.com"""

    @pytest.mark.smoke
    def test_valid_sign_up(self, driver, user_data_factory, user_cleanup, user_api):
        """Verify a new user can sign up via the UI and is persisted in the backend."""
        user = user_data_factory()
        user_cleanup(user)
        page = LoginAndSignUpPageClass(driver)
        logger.info(f"Starting signup test for user: {user.email}")

        page.navigate_to_url(BASE_URL)
        page.enter_signup_details(name=user.name, email_address=user.email)
        page.enter_account_information(user)
        page.create_account()

        assert page.is_account_created(), (
            f"Account creation confirmation not displayed for {user.email}"
        )
        logger.info(f"UI confirmation displayed for {user.email}")

        response = user_api.get_user_by_email(user.email)
        assert response.status_code == 200, (
            f"User API verification failed: expected 200, got {response.status_code}"
        )
        logger.info(f"API verified user exists: {user.email}")

    def test_valid_login(self, driver, registered_user):
        home_page = HomePageClass(driver)
        home_page.navigate_to_home_page()
        login_page = LoginAndSignUpPageClass(driver)
        login_page.login(registered_user.email, registered_user.password)
        assert home_page.header_component.get_logged_in_user_name() == registered_user.name, \
            "User log in failed"

    @pytest.mark.smoke
    @pytest.mark.parametrize("case_name, email, password, expected_error", [
        pytest.param("empty_password","testemail@gmail.com","", "valueMissing", id="empty_password"),
        pytest.param("invalid_email","test_email", "newpassword", "typeMismatch", id="invalid_email"),
        pytest.param("invalid_credentials","testemail@gmail.com", "password", "login_error", id="invalid_credentials"),
    ])
    def test_invalid_login(self, driver, email, password, case_name, expected_error):
        home_page = HomePageClass(driver)
        home_page.navigate_to_home_page()
        login_page = LoginAndSignUpPageClass(driver)
        login_page.login(email, password)

        if case_name == "empty_password":
            assert login_page.is_password_missing(), "Password not empty"
            assert login_page.get_password_validation_message(), "Password validation failed"
        if case_name == "invalid_email":
            assert login_page.is_username_valid(), "Email address validation failed"
            assert login_page.get_username_validation_message(), "Email address validation failed"
        if case_name == "invalid_credentials":
            expected_error = "Your email or password is incorrect!"
            assert login_page.get_login_error_message() == expected_error, "Login error message not displayed"


