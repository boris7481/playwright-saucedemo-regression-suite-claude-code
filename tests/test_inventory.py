from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from test_data.products import (
    ALL_PRODUCTS,
    SORT_NAME_A_TO_Z,
    SORT_NAME_Z_TO_A,
    SORT_PRICE_LOW_TO_HIGH,
    SORT_PRICE_HIGH_TO_LOW,
)


def test_inventory_displays_all_products(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    products = inventory.get_product_names()
    assert len(products) == 6
    for product in ALL_PRODUCTS:
        assert product in products


def test_sort_inventory_form_a_to_z(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.sort_by(SORT_NAME_A_TO_Z)
    products = inventory.get_product_names()
    expected_products = sorted(products)
    assert products == expected_products


def test_sort_inventory_form_z_to_a(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.sort_by(SORT_NAME_Z_TO_A)
    products = inventory.get_product_names()
    expected_products = sorted(products, reverse=True)
    assert products == expected_products


def test_sort_inventory_price_from_low_to_high(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.sort_by(SORT_PRICE_LOW_TO_HIGH)
    prices = inventory.get_product_prices()
    assert prices == sorted(prices)


def test_sort_inventory_price_from_high_to_low(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.sort_by(SORT_PRICE_HIGH_TO_LOW)
    prices = inventory.get_product_prices()
    assert prices == sorted(prices, reverse=True)
