from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_add_multiple_products_to_card(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.open_product("Sauce Labs Backpack")
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    authenticated_page.get_by_role("button", name="Back to products").click()
    expect(authenticated_page.get_by_text("Products")).to_be_visible()
    inventory.open_product("Sauce Labs Bike Light")
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text("Sauce Labs Bike Light")).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("2")


def test_add_single_product_to_card_and_verify_card_content(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.open_product("Sauce Labs Backpack")
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    inventory.go_to_cart()
    expect(authenticated_page.locator('[data-test="inventory-item-name"]')).to_have_text("Sauce Labs Backpack")
    expect(authenticated_page.locator('[data-test="item-quantity"]')).to_have_text("1")
    expect(authenticated_page.locator('[data-test="inventory-item-price"]')).to_have_text("$29.99")
    expect(authenticated_page.get_by_text("Continue Shopping")).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Remove")).to_be_visible()


def test_remove_product_from_cart(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.open_product("Sauce Labs Backpack")
    expect(authenticated_page.get_by_text("Back to products")).to_be_visible()
    expect(authenticated_page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    authenticated_page.get_by_role("button", name="Add to cart").click()
    expect(authenticated_page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    inventory.go_to_cart()
    expect(authenticated_page.locator('[data-test="inventory-item-name"]')).to_have_text("Sauce Labs Backpack")
    expect(authenticated_page.locator('[data-test="item-quantity"]')).to_have_text("1")
    expect(authenticated_page.locator('[data-test="inventory-item-price"]')).to_have_text("$29.99")
    expect(authenticated_page.get_by_text("Continue Shopping")).to_be_visible()
    expect(authenticated_page.get_by_role("button", name="Remove")).to_be_visible()
    cart = CartPage(authenticated_page)
    cart.remove_item("Sauce Labs Backpack")
    expect(authenticated_page.get_by_text("Sauce Labs Backpack")).not_to_be_visible()
