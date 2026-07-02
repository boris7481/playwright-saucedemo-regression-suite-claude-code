from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login_with_valid_username_and_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    expect(page.get_by_text("Products")).to_be_visible()


def test_login_with_valid_username_and_wrong_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "wrong_password")
    expect( page.get_by_text( "Epic sadface: Username and password do not match any user in this service")).to_be_visible()


def test_login_with_invalid_username_and_valid_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("wrong_username", "secret_sauce")
    expect(page.get_by_text("Epic sadface: Username and password do not match any user in this service")).to_be_visible()


def test_login_with_empty_fields_for_username_and_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("", "")
    expect(page.get_by_text("Epic sadface: Username is required")).to_be_visible()


def test_with_locked_user_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("locked_out_user", "secret_sauce")
    expect( page.get_by_text("Epic sadface: Sorry, this user has been locked out.") ).to_be_visible()
