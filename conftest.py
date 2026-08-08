import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from test_data.users import STANDARD_USER


@pytest.fixture
def authenticated_page(page: Page, base_url: str) -> Page:
    page.goto(base_url)
    page.get_by_placeholder("Username").fill(STANDARD_USER["username"])
    page.get_by_placeholder("Password").fill(STANDARD_USER["password"])
    page.get_by_role("button", name="login").click()
    page.get_by_text("Products").wait_for()
    yield page


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(authenticated_page: Page) -> InventoryPage:
    return InventoryPage(authenticated_page)


@pytest.fixture
def cart_page(authenticated_page: Page) -> CartPage:
    return CartPage(authenticated_page)


@pytest.fixture
def checkout_page(authenticated_page: Page) -> CheckoutPage:
    return CheckoutPage(authenticated_page)




