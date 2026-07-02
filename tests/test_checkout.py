from playwright.sync_api import Page, expect


def test_checkout_complete(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.get_by_text("Sauce Labs Backpack").click()
    expect(page.get_by_text("Back to products")).to_be_visible()
    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    page.get_by_role("button", name="Add to cart").click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-badge"]').click()
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        "Sauce Labs Backpack"
    )
    expect(page.get_by_text("Continue Shopping")).to_be_visible()
    page.get_by_role("button", name="Checkout").click()
    expect(page.get_by_text("Checkout: Your Information")).to_be_visible()
    page.get_by_placeholder("First Name").fill("standard_user")
    page.get_by_placeholder("Last Name").fill("last_check")
    page.get_by_placeholder("Zip/Postal Code").fill("81450")
    page.get_by_role("button", name="Continue").click()
    expect(page.get_by_text("Checkout: Overview")).to_be_visible()
    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    expect(page.locator('[data-test="item-quantity"]')).to_have_text("1")
    expect(page.locator('[data-test="inventory-item-price"]')).to_have_text("$29.99")
    expect(page.get_by_text("SauceCard #31337")).to_be_visible()
    expect(page.get_by_text("Free Pony Express Delivery!")).to_be_visible()
    expect(page.get_by_text("Item total: $29.99")).to_be_visible()
    expect(page.get_by_text("Tax: $2.40")).to_be_visible()
    expect(page.get_by_text("Total: $32.39")).to_be_visible()
    price = 29.99
    tax = 2.40
    expected_total = price + tax
    assert expected_total == 32.39

    expect(page.get_by_role("button", name="Finish")).to_be_visible()
    expect(page.get_by_role("button", name="Cancel")).to_be_visible()
    page.get_by_role("button", name="Finish").click()
    expect(page.get_by_text("Thank you for your order!")).to_be_visible()


def test_checkout_first_name_required(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.get_by_text("Sauce Labs Backpack").click()
    expect(page.get_by_text("Back to products")).to_be_visible()
    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    page.get_by_role("button", name="Add to cart").click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-badge"]').click()
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        "Sauce Labs Backpack"
    )
    expect(page.get_by_text("Continue Shopping")).to_be_visible()
    page.get_by_role("button", name="Checkout").click()
    expect(page.get_by_text("Checkout: Your Information")).to_be_visible()
    page.get_by_placeholder("First Name").fill("")
    page.get_by_placeholder("Last Name").fill("last_check")
    page.get_by_placeholder("Zip/Postal Code").fill("81450")
    page.get_by_role("button", name="Continue").click()
    expect(page.get_by_text("Error: First Name is required")).to_be_visible()


def test_checkout_last_name_required(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.get_by_text("Sauce Labs Backpack").click()
    expect(page.get_by_text("Back to products")).to_be_visible()
    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    page.get_by_role("button", name="Add to cart").click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-badge"]').click()
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        "Sauce Labs Backpack"
    )
    expect(page.get_by_text("Continue Shopping")).to_be_visible()
    page.get_by_role("button", name="Checkout").click()
    expect(page.get_by_text("Checkout: Your Information")).to_be_visible()
    page.get_by_placeholder("First Name").fill("standard_user")
    page.get_by_placeholder("Last Name").fill("")
    page.get_by_placeholder("Zip/Postal Code").fill("81450")
    page.get_by_role("button", name="Continue").click()
    expect(page.get_by_text("Error: Last Name is required")).to_be_visible()


def test_checkout_postal_code_required(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.get_by_text("Sauce Labs Backpack").click()
    expect(page.get_by_text("Back to products")).to_be_visible()
    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    page.get_by_role("button", name="Add to cart").click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-badge"]').click()
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text(
        "Sauce Labs Backpack"
    )
    expect(page.get_by_text("Continue Shopping")).to_be_visible()
    page.get_by_role("button", name="Checkout").click()
    expect(page.get_by_text("Checkout: Your Information")).to_be_visible()
    page.get_by_placeholder("First Name").fill("standard_user")
    page.get_by_placeholder("Last Name").fill("last_check")
    page.get_by_placeholder("Zip/Postal Code").fill("")
    page.get_by_role("button", name="Continue").click()
    expect(page.get_by_text("Error: Postal Code is required")).to_be_visible()


def test_checkout_cancel(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.get_by_text("Sauce Labs Backpack").click()
    expect(page.get_by_text("Back to products")).to_be_visible()
    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    page.get_by_role("button", name="Add to cart").click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-badge"]').click()
    expect(page.locator('[data-test="inventory-item-name"]')).to_have_text("Sauce Labs Backpack")
    expect(page.get_by_text("Continue Shopping")).to_be_visible()
    page.get_by_role("button", name="Checkout").click()
    expect(page.get_by_text("Checkout: Your Information")).to_be_visible()
    page.get_by_placeholder("First Name").fill("standard_user")
    page.get_by_placeholder("Last Name").fill("last_check")
    page.get_by_placeholder("Zip/Postal Code").fill("81456")
    page.get_by_role("button", name="Continue").click()
    expect(page.get_by_text("Checkout: Overview")).to_be_visible()
    page.get_by_role("button", name="Cancel").click()
    expect(page.get_by_text("Products")).to_be_visible()
