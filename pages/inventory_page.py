import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object Model (POM) cho trang Danh sách sản phẩm (Inventory) SauceDemo."""

    # Locators
    TITLE = "[data-test='title']"
    INVENTORY_CONTAINER = "#inventory_container"
    INVENTORY_ITEM = "[data-test='inventory-item']"
    SHOPPING_CART_LINK = "[data-test='shopping-cart-link']"
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_SIDEBAR_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Lấy tiêu đề trang danh sách sản phẩm (vd: Products)")
    def get_header_title(self) -> str:
        """Lấy tiêu đề trang danh sách sản phẩm (vd: Products)."""
        return self.get_text(self.TITLE)

    @allure.step("Kiểm tra trang sản phẩm đã hiển thị thành công hay chưa")
    def is_inventory_displayed(self) -> bool:
        """Kiểm tra trang sản phẩm đã hiển thị thành công hay chưa."""
        try:
            # wait_for sẽ tự động chờ cho đến khi phần tử xuất hiện (tối đa 30s theo mặc định)
            self.page.locator(self.TITLE).wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    @allure.step("Đếm số lượng sản phẩm đang hiển thị")
    def get_items_count(self) -> int:
        """Đếm số lượng sản phẩm đang hiển thị."""
        return self.find(self.INVENTORY_ITEM).count()

    @allure.step("Đăng xuất khỏi tài khoản qua thanh điều hướng burger menu")
    def logout(self) -> None:
        """Đăng xuất khỏi tài khoản qua thanh điều hướng burger menu."""
        self.click(self.BURGER_MENU_BUTTON)
        self.wait_for_selector(self.LOGOUT_SIDEBAR_LINK, state="visible")
        self.click(self.LOGOUT_SIDEBAR_LINK)