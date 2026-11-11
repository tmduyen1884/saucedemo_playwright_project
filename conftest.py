import json
import os
import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Đảm bảo đường dẫn thư mục gốc dự án nằm trong sys.path để import dễ dàng
PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

STATE_FILE = PROJECT_ROOT / "data" / "state.json"


@pytest.fixture(scope="session")
def test_data():
    """Fixture tải dữ liệu kiểm thử từ file test_data.json."""
    data_file_path = PROJECT_ROOT / "data" / "test_data.json"
    with open(data_file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# -------------------------------------------------------------
# GIẢ LẬP THIẾT BỊ DI ĐỘNG (Mobile Device Emulation - iPhone 14 Pro Max)
# -------------------------------------------------------------
@pytest.fixture(scope="function")
def page_context():
    with sync_playwright() as p:
        # 1. Gọi bộ cấu hình của một thiết bị di động (ví dụ: iPhone 14 Pro Max)
        # Bạn có thể đổi thành 'Pixel 7', 'Galaxy S22', 'iPad Pro 11'...
        iphone_config = p.devices["iPhone 14 Pro Max"]

        # 2. Khởi tạo trình duyệt (headless=False để trực tiếp quan sát)
        browser = p.chromium.launch(headless=False)

        # 3. Trải phẳng (unpack) cấu hình iPhone vào context
        # Đồng thời bật chế độ Dark Mode (Giao diện tối)
        context = browser.new_context(
            **iphone_config,
            color_scheme="dark"
            # storage_state="data/state.json" # (Bỏ comment dòng này nếu bạn muốn kết hợp bỏ qua login)
        )

        page = context.new_page()
        page.goto("https://www.saucedemo.com/")

        yield page

        context.close()
        browser.close()


@pytest.fixture
def login_page(page_context):
    return LoginPage(page_context)


@pytest.fixture
def inventory_page(page_context):
    return InventoryPage(page_context)


# -------------------------------------------------------------
# CÁC FIXTURES TÁI SỬ DỤNG PHIÊN ĐĂNG NHẬP (state.json)
# -------------------------------------------------------------
@pytest.fixture
def logged_in_context():
    """Khởi tạo context nạp sẵn session đăng nhập từ data/state.json."""
    with sync_playwright() as p:
        iphone_config = p.devices["iPhone 14 Pro Max"]
        browser = p.chromium.launch(headless=False)
        storage_state_path = str(STATE_FILE) if STATE_FILE.exists() else "data/state.json"
        context = browser.new_context(
            **iphone_config,
            color_scheme="dark",
            storage_state=storage_state_path
        )
        yield context
        context.close()
        browser.close()


@pytest.fixture
def logged_in_page(logged_in_context):
    page = logged_in_context.new_page()
    yield page
    page.close()


@pytest.fixture
def logged_in_inventory_page(logged_in_page):
    logged_in_page.goto("https://www.saucedemo.com/inventory.html")
    return InventoryPage(logged_in_page)
