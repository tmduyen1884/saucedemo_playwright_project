import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object Model (POM) cho trang đăng nhập SauceDemo."""

    URL = "https://www.saucedemo.com/"

    # Locators
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Mở trang đăng nhập SauceDemo")
    def load(self, url: str = None) -> None:
        """Mở trang đăng nhập SauceDemo."""
        target_url = url or self.URL
        self.navigate(target_url)

    @allure.step("Nhập tên đăng nhập: {username}")
    def enter_username(self, username: str) -> None:
        """Nhập tên đăng nhập."""
        self.fill(self.USERNAME_INPUT, username)

    @allure.step("Nhập mật khẩu: {password}")
    def enter_password(self, password: str) -> None:
        """Nhập mật khẩu."""
        self.fill(self.PASSWORD_INPUT, password)

    @allure.step("Nhấn nút Login")
    def click_login(self) -> None:
        """Nhấn nút Login."""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Thực hiện chuỗi hành động đăng nhập nhanh với tài khoản '{username}'")
    def login(self, username: str, password: str) -> None:
        """Thực hiện chuỗi hành động đăng nhập nhanh."""
        if username:
            self.enter_username(username)
        else:
            self.fill(self.USERNAME_INPUT, "")
            
        if password:
            self.enter_password(password)
        else:
            self.fill(self.PASSWORD_INPUT, "")
            
        self.click_login()

    @allure.step("Lấy thông báo lỗi khi đăng nhập không thành công")
    def get_error_message(self) -> str:
        """Lấy thông báo lỗi khi đăng nhập không thành công."""
        return self.get_text(self.ERROR_MESSAGE)

    @allure.step("Kiểm tra thông báo lỗi có hiển thị hay không")
    def is_error_displayed(self) -> bool:
        """Kiểm tra thông báo lỗi có hiển thị hay không."""
        return self.is_visible(self.ERROR_MESSAGE)