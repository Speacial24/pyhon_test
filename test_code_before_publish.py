import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urban_routes_main_page import UrbanRoutesPage
from helpers import is_url_reachable  # Importing the helper function
from data import URBAN_ROUTES_URL  # Importing the URL constant


# Pytest Fixture for WebDriver
@pytest.fixture(scope="class")
def driver():
    # Setup WebDriver with desired capabilities
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=capabilities)
    driver.maximize_window()
    driver.get("https://example.com")  # Replace with the actual application URL
    yield driver
    driver.quit()


# Test Class
@pytest.mark.usefixtures("driver")
class TestTaxiOrder:
    @classmethod
    def setup_class(cls):
        # Check if the Urban Routes server is working
        if is_url_reachable(URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")
            exit()

        # Initialize WebDriver and Page Object
        cls.driver = webdriver.Chrome()
        cls.order_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self, driver):
        self.order_page.enter_from_location("123 Main St")
        self.order_page.enter_to_location("456 Elm St")

    def test_select_supportive_mode(self, driver):
        self.order_page.select_supportive_mode()

    def test_add_phone_number(self, driver):
        self.order_page.enter_phone_number("1234567890")

    def test_add_card_payment(self, driver):
        self.order_page.select_card_payment_method()

    def test_add_message_to_driver(self, driver):
        self.order_page.enter_message_to_driver("Please wait 5 minutes.")

    def test_order_blanket_and_handkerchiefs(self, driver):
        self.order_page.add_blanket()
        self.order_page.add_handkerchiefs()

    def test_add_ice_creams(self, driver):
        self.order_page.add_ice_creams(count=2)

    def test_place_order(self, driver):
        self.order_page.place_order()
        success_message = self.order_page.get_success_message()
        assert "Order placed successfully" in success_message, \
            f"Expected 'Order placed successfully', but got '{success_message}'"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
