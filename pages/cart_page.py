from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    """
    Page Object representing the cart page (/cart.html).
    Responsibilities: navigation, reading cart contents, removing items,
    navigating to checkout or back to inventory.
    No assertions. No knowledge of adjacent pages.
    """

    URL = "/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Locators over lists — multiple items possible.
        self.item_names = self.page.locator('[data-test="inventory-item-name"]')
        self.item_quantities = self.page.locator('[data-test="item-quantity"]')
        self.item_prices = self.page.locator('[data-test="inventory-item-price"]')

        # Locators over single elements — global action buttons.
        self.checkout_button = self.page.get_by_role("button", name="Checkout")
        self.continue_shopping_button = self.page.get_by_role("button", name="Continue Shopping")

    def open(self) -> None:
        # Navigates to /cart.html via BasePage.navigate().
        # Requires base_url to be configured in pytest.ini.
        self.navigate(self.URL)

    def get_item_names(self) -> list[str]:
        # Returns the names of all items currently in the cart.
        # Returns an empty list if the cart is empty.
        return self.item_names.all_text_contents()

    def get_item_quantity(self, name: str) -> int:
        # Returns the quantity of a specific item as an integer.
        # Resolves the quantity within the targeted item's container
        # to avoid ambiguity with other items.
        # Kept deliberately, to keep the framework extensible —
        # SauceDemo currently always returns 1, but this method
        # will be useful once a variable-quantity scenario is tested.
        quantity = (
            self.page.locator(".cart_item")
            .filter(has_text=name)
            .locator('[data-test="item-quantity"]')
            .inner_text()
        )
        return int(quantity)

    def get_item_price(self, name: str) -> float:
        # Returns the price of a specific item as a float.
        # The "$29.99" → 29.99 conversion belongs in the Page Object,
        # not the test — consistent with InventoryPage.get_product_prices().
        price = (
            self.page.locator(".cart_item")
            .filter(has_text=name)
            .locator('[data-test="inventory-item-price"]')
            .inner_text()
        )
        return float(price.replace("$", ""))

    def remove_item(self, name: str) -> None:
        # Clicks the "Remove" button of the item targeted by name.
        # .cart_item is the actual item container on /cart.html —
        # SauceDemo doesn't expose a data-test attribute on this container.
        # filter(has_text=name) guarantees the right button even with
        # several items in the cart.
        self.page.locator(".cart_item").filter(
            has_text=name
        ).get_by_role("button", name="Remove").click()

    def checkout(self) -> None:
        # Clicks the "Checkout" button to navigate to the checkout page.
        # Short name, consistent with the other framework methods.
        # The test verifies what happens next — CartPage doesn't know.
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        # Clicks "Continue Shopping" to return to /inventory.html.
        # The test handles the rest of the navigation.
        self.continue_shopping_button.click()






