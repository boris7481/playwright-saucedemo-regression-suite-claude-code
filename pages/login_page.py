from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object representing the SauceDemo login page.
    Responsibilities: navigating to / and submitting the form.
    No assertions. No knowledge of the login outcome.
    """

    URL = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = self.page.get_by_placeholder("Username")
        self.password_input = self.page.get_by_placeholder("Password")
        self.login_button = self.page.get_by_role("button", name="Login")

    def open(self) -> None:
        # Navigates to the login page via BasePage.navigate().
        # The path is resolved against pytest-base-url's base_url.
        self.navigate(self.URL)

    def login(self, username: str, password: str) -> None:
        # Fills in the form and submits it.
        # No assertion on the outcome — that's the test's responsibility.
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()


