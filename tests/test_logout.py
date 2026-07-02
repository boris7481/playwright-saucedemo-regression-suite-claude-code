from playwright.sync_api import Page, expect


def test_logout_standard(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    page.get_by_role("button", name="Open Menu").click()
    page.get_by_role("link", name="Logout").click()
    expect(page.get_by_text("Accepted usernames are:")).to_be_visible()
    expect(page.get_by_text("Password for all users:")).to_be_visible()
