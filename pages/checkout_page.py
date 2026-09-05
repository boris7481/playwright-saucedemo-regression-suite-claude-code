from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Page Object covering the entire checkout flow:
    - /checkout-step-one.html  : customer information form
    - /checkout-step-two.html  : order summary
    - /checkout-complete.html  : order confirmation
    No assertions. No knowledge of adjacent pages.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Step 1 — information form
        self.first_name_input = self.page.get_by_placeholder("First Name")
        self.last_name_input = self.page.get_by_placeholder("Last Name")
        self.postal_code_input = self.page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = self.page.get_by_role("button", name="Continue")

        # Step 2 — summary and actions
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
        # Fills in only the three form fields.
        # Does not click Continue — call continue_checkout() separately.
        # This separation keeps form-validation tests atomic:
        # a test can partially fill the fields and then call
        # continue_checkout() to verify the expected error message.
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_checkout(self) -> None:
        # Clicks the "Continue" button to submit the step 1 form.
        # Called after fill_information(). If a field is empty or invalid,
        # the application stays on step 1 with an error message —
        # expected behavior for validation tests.
        self.continue_button.click()

    def get_item_total(self) -> float:
        # Returns the item subtotal as a float.
        # The label reads "Item total: $29.99" — split("$") extracts "29.99".
        # More robust than replace() if the label text changes.
        return float(self.item_total_label.inner_text().split("$")[-1])

    def get_tax(self) -> float:
        # Returns the tax amount as a float.
        # Same parsing strategy as get_item_total().
        return float(self.tax_label.inner_text().split("$")[-1])

    def get_total(self) -> float:
        # Returns the total (tax included) as a float.
        # The test can verify: assert checkout.get_total() ==
        # round(checkout.get_item_total() + checkout.get_tax(), 2)
        return float(self.total_label.inner_text().split("$")[-1])

    def finish(self) -> None:
        # Clicks "Finish" to confirm the order.
        # The test verifies the confirmation page after this call.
        self.finish_button.click()

    def cancel(self) -> None:
        # Clicks "Cancel" — available on both step 1 and step 2.
        # Returns to /inventory.html in both cases on SauceDemo.
        self.cancel_button.click()

    def get_confirmation_message(self) -> str:
        # Returns the confirmation header text.
        # The test does: assert checkout.get_confirmation_message() ==
        # "Thank you for your order!"
        return self.confirmation_header.inner_text()

    def go_back_home(self) -> None:
        # Clicks "Back Home" from the confirmation page.
        # Returns to /inventory.html.
        self.back_home_button.click()


