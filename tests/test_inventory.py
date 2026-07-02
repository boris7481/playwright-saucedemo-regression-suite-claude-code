from playwright.sync_api import Page

from pages.inventory_page import InventoryPage


def test_inventory_displays_all_products(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    products = inventory.get_product_names()
    assert len(products) == 6
    expected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)"
        ]
    for product in expected_products:
        assert product in products


def test_sort_inventory_form_a_to_z(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.sort_by("Name (A to Z)")
    products = inventory.get_product_names()
    expected_products = sorted(products)
    assert products == expected_products


def test_sort_inventory_form_z_to_a(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.sort_by("Name (Z to A)")
    products = inventory.get_product_names()
    expected_products = sorted(products, reverse=True)
    assert products == expected_products


def test_sort_inventory_price_from_low_to_high(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.sort_by("Price (low to high)")
    prices = inventory.get_product_prices()
    assert prices == sorted(prices)


def test_sort_inventory_price_from_high_to_low(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.sort_by("Price (high to low)")
    prices = inventory.get_product_prices()
    assert prices == sorted(prices, reverse=True)
