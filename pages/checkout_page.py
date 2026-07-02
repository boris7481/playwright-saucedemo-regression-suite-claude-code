from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Page Object couvrant l'ensemble du tunnel de commande :
    - /checkout-step-one.html  : formulaire d'informations client
    - /checkout-step-two.html  : récapitulatif de commande
    - /checkout-complete.html  : confirmation de commande
    Aucune assertion. Aucune connaissance des pages adjacentes.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Step 1 — formulaire d'informations
        self.first_name_input = self.page.get_by_placeholder("First Name")
        self.last_name_input = self.page.get_by_placeholder("Last Name")
        self.postal_code_input = self.page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = self.page.get_by_role("button", name="Continue")

        # Step 2 — récapitulatif et actions
        self.finish_button = self.page.get_by_role("button", name="Finish")
        self.cancel_button = self.page.get_by_role("button", name="Cancel")
        self.item_total_label = self.page.locator('[data-test="subtotal-label"]')
        self.tax_label = self.page.locator('[data-test="tax-label"]')
        self.total_label = self.page.locator('[data-test="total-label"]')

        # Step complete — confirmation
        self.confirmation_header = self.page.locator('[data-test="complete-header"]')
        self.back_home_button = self.page.get_by_role("button", name="Back Home")

    def fill_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        # Remplit uniquement les trois champs du formulaire.
        # Ne clique pas sur Continue — appeler continue_checkout() séparément.
        # Cette séparation rend les tests de validation du formulaire atomiques :
        # un test peut remplir partiellement les champs puis appeler
        # continue_checkout() pour vérifier le message d'erreur attendu.
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_checkout(self) -> None:
        # Clique sur le bouton "Continue" pour soumettre le formulaire step 1.
        # Appelé après fill_information(). Si un champ est vide ou invalide,
        # l'application reste sur step 1 avec un message d'erreur —
        # comportement attendu pour les tests de validation.
        self.continue_button.click()

    def get_item_total(self) -> float:
        # Retourne le sous-total des articles sous forme de float.
        # Le label s'affiche "Item total: $29.99" — split("$") extrait "29.99".
        # Plus robuste que replace() si le texte du label évolue.
        return float(self.item_total_label.inner_text().split("$")[-1])

    def get_tax(self) -> float:
        # Retourne le montant des taxes sous forme de float.
        # Même stratégie de parsing que get_item_total().
        return float(self.tax_label.inner_text().split("$")[-1])

    def get_total(self) -> float:
        # Retourne le total TTC sous forme de float.
        # Le test peut vérifier : assert checkout.get_total() ==
        # round(checkout.get_item_total() + checkout.get_tax(), 2)
        return float(self.total_label.inner_text().split("$")[-1])

    def finish(self) -> None:
        # Clique sur "Finish" pour confirmer la commande.
        # Le test vérifie la page de confirmation après cet appel.
        self.finish_button.click()

    def cancel(self) -> None:
        # Clique sur "Cancel" — disponible sur step 1 et step 2.
        # Retourne vers /inventory.html dans les deux cas sur SauceDemo.
        self.cancel_button.click()

    def get_confirmation_message(self) -> str:
        # Retourne le texte du header de confirmation.
        # Le test fait : assert checkout.get_confirmation_message() ==
        # "Thank you for your order!"
        return self.confirmation_header.inner_text()

    def go_back_home(self) -> None:
        # Clique sur "Back Home" depuis la page de confirmation.
        # Retourne vers /inventory.html.
        self.back_home_button.click()
