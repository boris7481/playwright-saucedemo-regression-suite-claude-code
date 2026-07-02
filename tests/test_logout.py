from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage


def test_logout_standard(authenticated_page: Page):
    inventory = InventoryPage(authenticated_page)
    inventory.open_menu()
    inventory.logout()
    expect(authenticated_page.get_by_text("Accepted usernames are:")).to_be_visible()
    expect(authenticated_page.get_by_text("Password for all users:")).to_be_visible()
