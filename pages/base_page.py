from playwright.sync_api import Page, Locator


class BasePage:
    """
    Base class shared by all Page Objects.
    Contains only strictly cross-cutting behavior.
    Any page-specific logic belongs in the subclass.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, path: str = "") -> None:
        # Accepts a relative path ("/inventory.html") or an empty one ("/").
        # The base URL is handled by pytest-base-url in conftest.py.
        self.page.goto(path)

    def is_visible(self, locator: Locator) -> bool:
        # Returns a boolean, never raises.
        # State check — not a test assertion.
        return locator.is_visible()

    def open_menu(self) -> None:
        # Opens the hamburger menu — available on every page.
        # Must be called before logout() — the two actions are kept separate
        # per the one-method-one-action principle.
        self.page.get_by_role("button", name="Open Menu").click()

    def logout(self) -> None:
        # Clicks the "Logout" link in the hamburger menu.
        # Requires open_menu() to have been called first.
        self.page.get_by_role("link", name="Logout").click()






