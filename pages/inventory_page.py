from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """
    Page Object représentant la page inventory (/inventory.html).
    Responsabilités : navigation, lecture des produits, tri, ajout au panier.
    Aucune assertion. Aucune connaissance des pages suivantes.
    """

    URL = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Locators sur des listes — retournent N éléments.
        # Résolus via all_text_contents() dans les méthodes.
        self.product_names = self.page.locator('[data-test="inventory-item-name"]')
        self.product_prices = self.page.locator('[data-test="inventory-item-price"]')

        # Locators sur des éléments uniques.
        self.sort_dropdown = self.page.locator('[data-test="product-sort-container"]')
        self.cart_badge = self.page.locator('[data-test="shopping-cart-badge"]')

    def open(self) -> None:
        # Navigue vers /inventory.html via BasePage.navigate().
        # Requiert que base_url soit configuré dans pytest.ini.
        self.navigate(self.URL)

    def get_product_names(self) -> list[str]:
        # Retourne tous les noms de produits visibles sous forme de liste.
        # Le test fait ses propres assertions sur cette liste.
        return self.product_names.all_text_contents()

    def get_product_prices(self) -> list[float]:
        # Retourne les prix sous forme de floats — le "$" est retiré ici.
        # La conversion string→float appartient au Page Object :
        # c'est de la mécanique UI, pas de la logique de test.
        raw = self.product_prices.all_text_contents()
        return [float(price.replace("$", "")) for price in raw]

    def sort_by(self, option: str) -> None:
        # Sélectionne une option de tri par son label visible.
        # label= garantit la sélection par texte affiché, pas par valeur interne.
        # Exemples : "Name (A to Z)", "Price (low to high)"
        self.sort_dropdown.select_option(label=option)

    def open_product(self, name: str) -> None:
        # Clique sur un produit par son nom pour ouvrir sa page détail.
        # get_by_text() est approprié ici : le nom est unique sur la page.
        self.page.get_by_text(name).click()

    def add_to_cart(self, name: str) -> None:
        # Résout dynamiquement le bouton "Add to cart" du produit ciblé.
        # filter() cible le conteneur du produit dont le nom correspond,
        # puis remonte au bouton dans ce contexte — évite l'ambiguïté
        # entre les 6 boutons identiques présents sur la page.
        self.page.locator('[data-test="inventory-item"]').filter(
            has_text=name
        ).get_by_role("button", name="Add to cart").click()

    def get_cart_count(self) -> int:
        # Retourne le compteur du panier sous forme d'entier.
        # Retourne 0 si le badge n'est pas visible — le badge disparaît
        # du DOM quand le panier est vide, inner_text() lèverait une exception.
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.inner_text())
