import json
from pathlib import Path
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Đọc dữ liệu test từ data/test_data.json để sử dụng cho parametrize
DATA_PATH = Path(__file__).parent.parent / "data" / "test_data.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    TEST_DATA = json.load(f)


class TestLogin:
    """Bộ kiểm thử chức năng Đăng nhập trên trang SauceDemo."""

    def test_login_success(self, login_page: LoginPage, inventory_page: InventoryPage, test_data):
        """TC01: Đăng nhập thành công với tài khoản hợp lệ."""
        valid_user = test_data["valid_user"]

        login_page.login(valid_user["username"], valid_user["password"])

        # Kiểm tra chuyển hướng thành công đến trang sản phẩm
        assert "inventory.html" in inventory_page.get_url()
        assert inventory_page.is_inventory_displayed()
        assert inventory_page.get_header_title() == "Products"
        assert inventory_page.get_items_count() > 0

    def test_login_locked_out_user(self, login_page: LoginPage, test_data):
        """TC02: Đăng nhập với tài khoản bị khóa (locked_out_user)."""
        locked_user = test_data["locked_out_user"]

        login_page.login(locked_user["username"], locked_user["password"])

        # Kiểm tra hiển thị thông báo lỗi chính xác
        assert login_page.is_error_displayed()
        assert login_page.get_error_message() == locked_user["expected_error"]

    @pytest.mark.parametrize(
        "case",
        TEST_DATA["invalid_credentials"],
        ids=[c["case_name"] for c in TEST_DATA["invalid_credentials"]]
    )
    def test_login_invalid_credentials(self, login_page: LoginPage, case):
        """TC03: Data-Driven Testing cho các trường hợp đăng nhập không hợp lệ."""
        login_page.login(case["username"], case["password"])

        # Xác thực thông báo lỗi hiển thị đúng với từng trường hợp
        assert login_page.is_error_displayed()
        assert login_page.get_error_message() == case["expected_error"]

    def test_logout_success(self, login_page: LoginPage, inventory_page: InventoryPage, test_data):
        """TC04: Đăng nhập thành công sau đó đăng xuất."""
        valid_user = test_data["valid_user"]

        login_page.login(valid_user["username"], valid_user["password"])
        assert inventory_page.is_inventory_displayed()

        inventory_page.logout()

        # Kiểm tra đã quay về trang đăng nhập
        login_page.page.locator(login_page.LOGIN_BUTTON).wait_for(state="visible", timeout=5000)
