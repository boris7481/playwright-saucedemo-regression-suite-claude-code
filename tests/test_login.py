import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from test_data.users import STANDARD_USER, LOCKED_OUT_USER, INVALID_USERNAME, WRONG_PASSWORD, EMPTY_CREDENTIALS
from test_data.messages import (
    LOGIN_ERROR_INVALID_CREDENTIALS,
    LOGIN_ERROR_USERNAME_REQUIRED,
    LOGIN_ERROR_LOCKED_OUT,
)


def test_login_with_valid_username_and_password(page: Page, login_page: LoginPage):
    login_page.open()
    login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])
    expect(page.get_by_text("Products")).to_be_visible()


@pytest.mark.parametrize(
    "user, expected_error",
    [
        (WRONG_PASSWORD, LOGIN_ERROR_INVALID_CREDENTIALS),
        (INVALID_USERNAME, LOGIN_ERROR_INVALID_CREDENTIALS),
        (EMPTY_CREDENTIALS, LOGIN_ERROR_USERNAME_REQUIRED),
        (LOCKED_OUT_USER, LOGIN_ERROR_LOCKED_OUT),
    ],
    ids=["wrong_password", "invalid_username", "empty_fields", "locked_out_user"],
)
def test_login_with_invalid_credentials(
    page: Page, login_page: LoginPage, user: dict, expected_error: str
):
    login_page.open()
    login_page.login(user["username"], user["password"])
    expect(page.get_by_text(expected_error)).to_be_visible()






