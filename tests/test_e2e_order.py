from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from test_data.products import BACKPACK, BACKPACK_PRICE
from test_data.checkout_info import VALID_CUSTOMER
from test_data.messages import CHECKOUT_SUCCESS_ORDER_CONFIRMATION


def test_complete_order_flow(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    cart = CartPage(authenticated_page)
    checkout = CheckoutPage(authenticated_page)
    inventory.open_product(BACKPACK)
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text(BACKPACK)).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    inventory.go_to_cart()
    expect(authenticated_page.locator('[data-test="inventory-item-name"]')).to_have_text(BACKPACK)
    expect(authenticated_page.get_by_text("Continue Shopping")).to_be_visible()
    cart.checkout()
    expect(authenticated_page.get_by_text("Checkout: Your Information")).to_be_visible()
    checkout.fill_information(
        VALID_CUSTOMER["first_name"], VALID_CUSTOMER["last_name"], VALID_CUSTOMER["postal_code"]
    )
    checkout.continue_checkout()
    expect(authenticated_page.get_by_text("Checkout: Overview")).to_be_visible()
    expect(authenticated_page.get_by_text(BACKPACK)).to_be_visible()
    expect(authenticated_page.locator('[data-test="item-quantity"]')).to_have_text("1")
    expect(authenticated_page.locator('[data-test="inventory-item-price"]')).to_have_text(f"${BACKPACK_PRICE}")
    expect(authenticated_page.get_by_text("SauceCard #31337")).to_be_visible()
    expect(authenticated_page.get_by_text("Free Pony Express Delivery!")).to_be_visible()
    expect(authenticated_page.get_by_text("Item total: $29.99")).to_be_visible()
    expect(authenticated_page.get_by_text("Tax: $2.40")).to_be_visible()
    expect(authenticated_page.get_by_text("Total: $32.39")).to_be_visible()
    price = BACKPACK_PRICE
    tax = 2.40
    expected_total = price + tax
    assert expected_total == 32.39
    expect(authenticated_page.get_by_role("button", name="Finish")).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Cancel")).to_be_visible()
    checkout.finish()
    expect(authenticated_page.get_by_text(CHECKOUT_SUCCESS_ORDER_CONFIRMATION)).to_be_visible()
    checkout.go_back_home()
    expect(authenticated_page.get_by_text("Products")).to_be_visible()
    inventory.open_menu()
    inventory.logout()
    expect(authenticated_page.get_by_text("Accepted usernames are:")).to_be_visible()
    expect(authenticated_page.get_by_text("Password for all users:")).to_be_visible()
