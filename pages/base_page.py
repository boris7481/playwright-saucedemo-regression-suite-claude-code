from playwright.sync_api import Page, Locator


class BasePage:
    """
    Classe parente commune à tous les Page Objects.
    Ne contient que des comportements strictement transverses.
    Toute logique spécifique à une page appartient à la sous-classe.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, path: str = "") -> None:
        # Reçoit un chemin relatif ("/inventory.html") ou vide ("/").
        # La base URL est gérée par pytest-base-url dans conftest.py.
        self.page.goto(path)

    def is_visible(self, locator: Locator) -> bool:
        # Retourne un booléen, ne lève pas d'exception.
        # Interrogation d'état — pas une assertion de test.
        return locator.is_visible()

    def open_menu(self) -> None:
        # Ouvre le menu hamburger — disponible sur toutes les pages.
        # Doit être appelée avant logout() — les deux actions sont séparées
        # conformément au principe : une méthode = une action.
        self.page.get_by_role("button", name="Open Menu").click()

    def logout(self) -> None:
        # Clique sur le lien "Logout" dans le menu hamburger.
        # Requiert que open_menu() ait été appelée au préalable.
        self.page.get_by_role("link", name="Logout").click()
