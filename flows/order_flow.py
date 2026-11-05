from models.payment_card import PaymentCard
from pages.cart_page import CartPageClass
from pages.checkout_page import CheckoutPageClass
from pages.components.checkout_modal import CheckoutModalClass
from pages.home_page import HomePageClass
from pages.login_and_signup_page import LoginAndSignUpPageClass
from pages.payment_page import PaymentPageClass


class OrderFlow:
    def __init__(self, driver):
        self.home_page = HomePageClass(driver)
        self.cart_page = CartPageClass(driver)
        self.checkout_modal = CheckoutModalClass(driver)
        self.login_page = LoginAndSignUpPageClass(driver)
        self.checkout_page = CheckoutPageClass(driver)
        self.payment_page = PaymentPageClass(driver)

    # Navigation and cart steps
    def open_home_page(self):
        self.home_page.navigate_to_home_page()

    def add_product_to_cart(self):
        self.open_home_page()
        self.home_page.add_featured_product_to_cart()

    def view_cart_from_modal(self):
        self.home_page.cart_modal.click_view_cart()

    def open_cart_from_header(self):
        self.cart_page.header_component.navigate_to_cart_page()

    def proceed_to_checkout(self):
        self.cart_page.proceed_to_checkout()

    # Login and registration steps
    def open_login_page(self):
        # Replace with whatever your header/home page uses to open the login page
        self.login_page.header_component.navigate_to_login_page()

    def login(self, user):
        self.login_page.login(user.email, user.password)

    def register_user(self, user_data):
        self.login_page.enter_signup_details(
            name=user_data.name, email_address=user_data.email
        )
        self.login_page.enter_account_information(user_data)
        self.login_page.create_account()

    def get_logged_in_user_name(self):
        return self.login_page.header_component.get_logged_in_user_name()

    # Order steps
    def place_order_and_pay(self, card: PaymentCard):
        self.checkout_page.place_order()
        self.payment_page.enter_card_details(
            card.name, card.number, card.cvc, card.expiry_month, card.expiry_year
        )
        self.payment_page.pay_and_confirm_order()
        return self.payment_page.is_order_placed_successfully()