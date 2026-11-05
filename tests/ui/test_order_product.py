import pytest

from models.payment_card import PaymentCard


@pytest.mark.ui
class TestOrderProducts:

    def test_order_products_register_while_checkout(
        self, order_flow, user_data_factory, user_cleanup
    ):
        """Verifies signup is required if a guest user tries to order a product"""
        user_data = user_data_factory()
        user_cleanup(user_data)

        order_flow.add_product_to_cart()
        assert order_flow.home_page.cart_modal.is_visible(), \
            "Cart modal did not appear on home page after adding product to cart"

        order_flow.view_cart_from_modal()
        order_flow.proceed_to_checkout()
        assert order_flow.checkout_modal.is_visible(), \
            "Checkout modal did not appear for guest user to login/register"

        order_flow.checkout_modal.click_register_login()
        order_flow.register_user(user_data)
        assert order_flow.login_page.is_account_created(), "Account creation failed"

        order_flow.open_home_page()
        actual_name = order_flow.get_logged_in_user_name()
        assert actual_name == user_data.name, \
            f"Expected '{user_data.name}' to be logged in, but header shows '{actual_name}'"

        order_flow.open_cart_from_header()
        order_flow.proceed_to_checkout()
        assert not order_flow.checkout_modal.is_visible(), \
            "Checkout modal still appears for a logged-in user"
        assert order_flow.checkout_page.is_checkout_page_visible(), \
            "Checkout page did not appear for logged-in user"

        order_placed = order_flow.place_order_and_pay(PaymentCard(name=user_data.name))
        assert order_placed, "Order was not placed successfully"

    def test_order_products_login_while_checkout(self, order_flow, registered_user):
        """Verifies login is required for buying a product if the user is already registered"""
        order_flow.add_product_to_cart()
        assert order_flow.home_page.cart_modal.is_visible(), \
            "Cart modal did not appear on home page after adding product to cart"

        order_flow.view_cart_from_modal()
        order_flow.proceed_to_checkout()
        assert order_flow.checkout_modal.is_visible(), \
            "Checkout modal did not appear for guest user to login/register"

        order_flow.checkout_modal.click_register_login()
        order_flow.login(registered_user)
        actual_name = order_flow.get_logged_in_user_name()
        assert actual_name == registered_user.name, \
            f"Expected '{registered_user.name}' to be logged in, but header shows '{actual_name}'"

        order_flow.open_home_page()
        order_flow.open_cart_from_header()
        order_flow.proceed_to_checkout()
        assert order_flow.checkout_page.is_checkout_page_visible(), \
            "Checkout page did not appear for logged-in user"

        order_placed = order_flow.place_order_and_pay(PaymentCard(name=registered_user.name))
        assert order_placed, "Order was not placed successfully"

    def test_order_products_after_login(self, order_flow, registered_user):
        """Verifies a user who logs in first can add a product and order it"""
        order_flow.open_home_page()
        order_flow.open_login_page()
        order_flow.login(registered_user)
        actual_name = order_flow.get_logged_in_user_name()
        assert actual_name == registered_user.name, \
            f"Expected '{registered_user.name}' to be logged in, but header shows '{actual_name}'"

        order_flow.add_product_to_cart()
        assert order_flow.home_page.cart_modal.is_visible(), \
            "Cart modal did not appear on home page after adding product to cart"

        order_flow.view_cart_from_modal()
        order_flow.proceed_to_checkout()
        assert order_flow.checkout_page.is_checkout_page_visible(), \
            "Checkout page did not appear for logged-in user"

        order_placed = order_flow.place_order_and_pay(PaymentCard(name=registered_user.name))
        assert order_placed, "Order was not placed successfully"