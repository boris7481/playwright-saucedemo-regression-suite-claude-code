from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """
    Page Object representing the inventory page (/inventory.html).
    Responsibilities: navigation, reading products, sorting, adding to cart.
    No assertions. No knowledge of subsequent pages.
    """

    URL = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Locators over lists — resolve to N elements.
        # Resolved via all_text_contents() in the methods below.
        self.product_names = self.page.locator('[data-test="inventory-item-name"]')
        self.product_prices = self.page.locator('[data-test="inventory-item-price"]')

        # Locators over single elements.
        self.sort_dropdown = self.page.locator('[data-test="product-sort-container"]')
        self.cart_badge = self.page.locator('[data-test="shopping-cart-badge"]')

    def open(self) -> None:
        # Navigates to /inventory.html via BasePage.navigate().
        # Requires base_url to be configured in pytest.ini.
        self.navigate(self.URL)

    def get_product_names(self) -> list[str]:
        # Returns all visible product names as a list.
        # The test makes its own assertions on this list.
        return self.product_names.all_text_contents()

    def get_product_prices(self) -> list[float]:
        # Returns prices as floats — the "$" is stripped here.
        # The string-to-float conversion belongs in the Page Object:
        # it's UI mechanics, not test logic.
        raw = self.product_prices.all_text_contents()
        return [float(price.replace("$", "")) for price in raw]

    def sort_by(self, option: str) -> None:
        # Selects a sort option by its visible label.
        # label= guarantees selection by displayed text, not internal value.
        # Examples: "Name (A to Z)", "Price (low to high)"
        self.sort_dropdown.select_option(label=option)

    def open_product(self, name: str) -> None:
        # Clicks a product by its name to open its detail page.
        # get_by_text() is appropriate here: the name is unique on the page.
        self.page.get_by_text(name).click()

    def add_to_cart(self, name: str) -> None:
        # Dynamically resolves the "Add to cart" button for the targeted product.
        # filter() targets the container of the product whose name matches,
        # then scopes the button lookup to that context — avoids ambiguity
        # between the 6 identical buttons present on the page.
        self.page.locator('[data-test="inventory-item"]').filter(
            has_text=name
        ).get_by_role("button", name="Add to cart").click()

    def get_cart_count(self) -> int:
        # Returns the cart counter as an integer.
        # Returns 0 if the badge isn't visible — the badge is removed
        # from the DOM when the cart is empty, inner_text() would raise.
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.inner_text())

    def go_to_cart(self) -> None:
        # Clicks the cart badge to navigate to /cart.html.
        # Follows the real user journey — no direct URL navigation.
        self.cart_badge.click()









