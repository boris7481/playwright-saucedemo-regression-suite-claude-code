import pytest
from playwright.sync_api import Page

from test_data.users import STANDARD_USER


@pytest.fixture
def authenticated_page(page: Page, base_url: str) -> Page:
    page.goto(base_url)
    page.get_by_placeholder("Username").fill(STANDARD_USER["username"])
    page.get_by_placeholder("Password").fill(STANDARD_USER["password"])
    page.get_by_role("button", name="login").click()
    page.get_by_text("Products").wait_for()
    yield page
