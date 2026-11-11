import allure
from playwright.sync_api import Page, Locator


class BasePage:
    """Class cơ sở chứa các thao tác và phương thức tương tác chung với Playwright."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Điều hướng tới URL chỉ định: {url}")
    def navigate(self, url: str) -> None:
        """Điều hướng tới URL chỉ định."""
        self.page.goto(url)

    @allure.step("Lấy URL hiện tại của trang")
    def get_url(self) -> str:
        """Lấy URL hiện tại của trang."""
        return self.page.url

    @allure.step("Lấy title của trang hiện tại")
    def get_title(self) -> str:
        """Lấy title của trang hiện tại."""
        return self.page.title()

    @allure.step("Tìm một element dựa vào selector: {selector}")
    def find(self, selector: str) -> Locator:
        """Tìm một element dựa vào selector."""
        return self.page.locator(selector)

    @allure.step("Click vào phần tử theo selector: {selector}")
    def click(self, selector: str) -> None:
        """Click vào phần tử theo selector."""
        self.find(selector).click()

    @allure.step("Nhập văn bản '{text}' vào trường nhập liệu: {selector}")
    def fill(self, selector: str, text: str) -> None:
        """Nhập văn bản vào trường nhập liệu."""
        self.find(selector).fill(text)

    @allure.step("Lấy nội dung văn bản của phần tử: {selector}")
    def get_text(self, selector: str) -> str:
        """Lấy nội dung văn bản của phần tử."""
        return self.find(selector).inner_text()

    @allure.step("Kiểm tra phần tử {selector} có hiển thị trên giao diện hay không")
    def is_visible(self, selector: str, timeout: float = 5000) -> bool:
        """Kiểm tra phần tử có hiển thị trên giao diện hay không."""
        try:
            return self.find(selector).is_visible(timeout=timeout)
        except Exception:
            return False

    @allure.step("Chờ phần tử {selector} đạt trạng thái mong muốn: {state}")
    def wait_for_selector(self, selector: str, state: str = "visible", timeout: float = 5000) -> None:
        """Chờ phần tử đạt trạng thái mong muốn."""
        self.page.wait_for_selector(selector, state=state, timeout=timeout)