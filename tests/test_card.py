from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from test_data.products import BACKPACK, BIKE_LIGHT, BACKPACK_PRICE


def test_add_multiple_products_to_card(authenticated_page: Page, inventory_page: InventoryPage):
    inventory_page.open_product(BACKPACK)
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text(BACKPACK)).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    authenticated_page.get_by_role("button", name="Back to products").click()
    expect(authenticated_page.get_by_text("Products")).to_be_visible()
    inventory_page.open_product(BIKE_LIGHT)
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text(BIKE_LIGHT)).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("2")


def test_add_single_product_to_card_and_verify_card_content(authenticated_page: Page, inventory_page: InventoryPage):
    inventory_page.open_product(BACKPACK)
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text(BACKPACK)).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    inventory_page.go_to_cart()
    expect(authenticated_page.locator('[data-test="inventory-item-name"]')).to_have_text(BACKPACK)
    expect(authenticated_page.locator('[data-test="item-quantity"]')).to_have_text("1")
    expect(authenticated_page.locator('[data-test="inventory-item-price"]')).to_have_text(f"${BACKPACK_PRICE}")
    expect(authenticated_page.get_by_text("Continue Shopping")).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Remove")).to_be_visible()


def test_remove_product_from_cart(authenticated_page: Page, inventory_page: InventoryPage, cart_page: CartPage):
    inventory_page.open_product(BACKPACK)
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text(BACKPACK)).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    inventory_page.go_to_cart()
    expect(authenticated_page.locator('[data-test="inventory-item-name"]')).to_have_text(BACKPACK)
    expect(authenticated_page.locator('[data-test="item-quantity"]')).to_have_text("1")
    expect(authenticated_page.locator('[data-test="inventory-item-price"]')).to_have_text(f"${BACKPACK_PRICE}")
    expect(authenticated_page.get_by_text("Continue Shopping")).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Remove")).to_be_visible()
    cart_page.remove_item(BACKPACK)
    expect(authenticated_page.get_by_text(BACKPACK)).not_to_be_visible()
