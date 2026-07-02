from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object représentant la page de connexion de SauceDemo.
    Responsabilités : navigation vers / et soumission du formulaire.
    Aucune assertion. Aucune connaissance du résultat du login.
    """

    URL = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = self.page.get_by_placeholder("Username")
        self.password_input = self.page.get_by_placeholder("Password")
        self.login_button = self.page.get_by_role("button", name="Login")

    def open(self) -> None:
        # Navigue vers la page de login via BasePage.navigate().
        # Le chemin est résolu contre la base_url de pytest-base-url.
        self.navigate(self.URL)

    def login(self, username: str, password: str) -> None:
        # Remplit le formulaire et le soumet.
        # Aucune assertion sur le résultat — responsabilité du test.
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
