from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    """
    Page Object représentant la page panier (/cart.html).
    Responsabilités : navigation, lecture du contenu, suppression d'articles,
    navigation vers checkout ou retour inventory.
    Aucune assertion. Aucune connaissance des pages adjacentes.
    """

    URL = "/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Locators sur des listes — plusieurs articles possibles.
        self.item_names = self.page.locator('[data-test="inventory-item-name"]')
        self.item_quantities = self.page.locator('[data-test="item-quantity"]')
        self.item_prices = self.page.locator('[data-test="inventory-item-price"]')

        # Locators sur des éléments uniques — boutons d'action globaux.
        self.checkout_button = self.page.get_by_role("button", name="Checkout")
        self.continue_shopping_button = self.page.get_by_role("button", name="Continue Shopping")

    def open(self) -> None:
        # Navigue vers /cart.html via BasePage.navigate().
        # Requiert que base_url soit configuré dans pytest.ini.
        self.navigate(self.URL)

    def get_item_names(self) -> list[str]:
        # Retourne les noms de tous les articles présents dans le panier.
        # Retourne une liste vide si le panier est vide.
        return self.item_names.all_text_contents()

    def get_item_quantity(self, name: str) -> int:
        # Retourne la quantité d'un article spécifique sous forme d'entier.
        # Résout la quantité dans le contexte du conteneur de l'article ciblé
        # pour éviter toute ambiguïté avec d'autres articles.
        # Volontairement conservée pour rendre le framework extensible —
        # SauceDemo retourne actuellement toujours 1, mais cette méthode
        # sera utile dès qu'un scénario de quantité variable sera testé.
        quantity = (
            self.page.locator(".cart_item")
            .filter(has_text=name)
            .locator('[data-test="item-quantity"]')
            .inner_text()
        )
        return int(quantity)

    def get_item_price(self, name: str) -> float:
        # Retourne le prix d'un article spécifique sous forme de float.
        # La conversion "$29.99" → 29.99 appartient au Page Object,
        # pas au test — cohérent avec InventoryPage.get_product_prices().
        price = (
            self.page.locator(".cart_item")
            .filter(has_text=name)
            .locator('[data-test="inventory-item-price"]')
            .inner_text()
        )
        return float(price.replace("$", ""))

    def remove_item(self, name: str) -> None:
        # Clique sur le bouton "Remove" de l'article ciblé par son nom.
        # .cart_item est le conteneur réel des articles sur /cart.html —
        # SauceDemo n'expose pas de data-test sur ce conteneur.
        # filter(has_text=name) garantit le bon bouton même avec
        # plusieurs articles dans le panier.
        self.page.locator(".cart_item").filter(
            has_text=name
        ).get_by_role("button", name="Remove").click()

    def checkout(self) -> None:
        # Clique sur le bouton "Checkout" pour naviguer vers la page checkout.
        # Nom court et cohérent avec les autres méthodes du framework.
        # Le test vérifie ce qui se passe après — CartPage ne le sait pas.
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        # Clique sur "Continue Shopping" pour retourner sur /inventory.html.
        # Le test gère la suite de la navigation.
        self.continue_shopping_button.click()
