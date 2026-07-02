import pytest
from playwright.sync_api import Page


STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture
def authenticated_page(page: Page, base_url: str) -> Page:
    page.goto(base_url)
    page.get_by_placeholder("Username").fill(STANDARD_USER)
    page.get_by_placeholder("Password").fill(PASSWORD)
    page.get_by_role("button", name="login").click()
    page.get_by_text("Products").wait_for()
    yield page
