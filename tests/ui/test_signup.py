import logging

import pytest

from pages.login_and_signup_page import LoginAndSignUpPageClass

logger = logging.getLogger(__name__)


BASE_URL = "https://www.automationexercise.com/"


@pytest.mark.smoke
@pytest.mark.ui
class TestSignup:
    """Signup flow tests for automationexercise.com"""

    def test_valid_sign_up(self, driver, user_data_factory, user_api):
        """Verify a new user can sign up via the UI and is persisted in the backend."""
        user = user_data_factory()
        account_submitted = False

        try:
            page = LoginAndSignUpPageClass(driver)
            logger.info(f"Starting signup test for user: {user.email}")

            page.navigate_to_url(BASE_URL)
            page.enter_signup_details(name=user.name, email_address=user.email)
            page.enter_account_information(user)
            page.create_account()
            account_submitted = True

            assert page.is_account_created(), (
                f"Account creation confirmation not displayed for {user.email}"
            )
            logger.info(f"UI confirmation displayed for {user.email}")

            response = user_api.get_user_by_email(user.email)
            assert response.status_code == 200, (
                f"User API verification failed: expected 200, got {response.status_code}"
            )
            logger.info(f"API verified user exists: {user.email}")

        finally:
            if account_submitted:
                self._safe_delete_user(user_api, user)

    @staticmethod
    def _safe_delete_user(user_api, user):
        """Best-effort cleanup — never let teardown mask the real test failure."""
        try:
            delete_response = user_api.delete_user(email=user.email, password=user.password)
            if getattr(delete_response, "status_code", None) not in (200, 204):
                logger.warning(
                    f"Cleanup: delete_user for {user.email} returned "
                    f"{getattr(delete_response, 'status_code', 'unknown')}"
                )
            else:
                logger.info(f"Cleanup: deleted user {user.email}")

        except Exception as cleanup_error:
            logger.warning(f"Cleanup failed for {user.email}: {cleanup_error}")