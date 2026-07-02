from playwright.sync_api import Page, expect


def test_login_with_valid_username_and_password(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    products = page.locator(
        '[data-test="inventory-item-name"]'
    ).all_text_contents()
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

#   expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
#    expect(page.locator('[data-test="item-1-title-link"] [data-test="inventory-item-name"]')).to_have_text("Sauce Labs Bolt T-Shirt")
#   expect(page.get_by_text("Sauce Labs Bolt T-Shirt")).to_be_visible()
#   expect(page.get_by_text("Sauce Labs Onesie")).to_be_visible()
#   expect(page.get_by_text("Sauce Labs Bike Light")).to_be_visible()
#   expect(page.get_by_text("Sauce Labs Fleece Jacket")).to_be_visible()
#   expect(page.get_by_text("Test.allTheThings() T-Shirt (Red)")).to_be_visible()


def test_sort_inventory_form_a_to_z(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.locator('[data-test="product-sort-container"]').select_option("Name (A to Z)")
    products = page.locator('[data-test="inventory-item-name"]').all_text_contents()
    expected_products = sorted(products)
    assert products == expected_products


def test_sort_inventory_form_z_to_a(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.locator('[data-test="product-sort-container"]').select_option("Name (Z to A)")
    products = page.locator('[data-test="inventory-item-name"]').all_text_contents()
    expected_products = sorted(products, reverse=True)
    assert products == expected_products


def test_sort_inventory_price_from_low_to_high(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.locator('[data-test="product-sort-container"]').select_option( "Price (low to high)")
    prices = page.locator('[data-test="inventory-item-price"]').all_text_contents()
    prices = [float(price.replace("$", "")) for price in prices]
    assert prices == sorted(prices)


def test_sort_inventory_price_from_high_to_low(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.locator('[data-test="product-sort-container"]').select_option( "Price (high to low)")
    prices = page.locator('[data-test="inventory-item-price"]').all_text_contents()
    prices = [float(price.replace("$", "")) for price in prices]
    assert prices == sorted(prices, reverse=True)
