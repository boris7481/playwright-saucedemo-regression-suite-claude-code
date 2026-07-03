from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from test_data.users import STANDARD_USER, LOCKED_OUT_USER, INVALID_USERNAME, WRONG_PASSWORD, EMPTY_CREDENTIALS
from test_data.messages import (
    LOGIN_ERROR_INVALID_CREDENTIALS,
    LOGIN_ERROR_USERNAME_REQUIRED,
    LOGIN_ERROR_LOCKED_OUT,
)


def test_login_with_valid_username_and_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])
    expect(page.get_by_text("Products")).to_be_visible()


def test_login_with_valid_username_and_wrong_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(WRONG_PASSWORD["username"], WRONG_PASSWORD["password"])
    expect(page.get_by_text(LOGIN_ERROR_INVALID_CREDENTIALS)).to_be_visible()


def test_login_with_invalid_username_and_valid_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(INVALID_USERNAME["username"], INVALID_USERNAME["password"])
    expect(page.get_by_text(LOGIN_ERROR_INVALID_CREDENTIALS)).to_be_visible()


def test_login_with_empty_fields_for_username_and_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(EMPTY_CREDENTIALS["username"], EMPTY_CREDENTIALS["password"])
    expect(page.get_by_text(LOGIN_ERROR_USERNAME_REQUIRED)).to_be_visible()


def test_with_locked_user_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(LOCKED_OUT_USER["username"], LOCKED_OUT_USER["password"])
    expect(page.get_by_text(LOGIN_ERROR_LOCKED_OUT)).to_be_visible()
