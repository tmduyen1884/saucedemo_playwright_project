import json
import os
import sys
from pathlib import Path
import pytest
from playwright.sync_api import Page, Browser, Playwright
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
# Sử dụng trực tiếp fixture browser & playwright của pytest-playwright
# để tránh xung đột Asyncio Loop trên CI/CD (GitHub Actions)
# -------------------------------------------------------------
@pytest.fixture(scope="function")
def page_context(browser: Browser, playwright: Playwright):
    # 1. Gọi bộ cấu hình của thiết bị di động (iPhone 14 Pro Max)
    iphone_config = playwright.devices["iPhone 14 Pro Max"]

    # 2. Tạo context với cấu hình iPhone và Dark Mode
    context = browser.new_context(
        **iphone_config,
        color_scheme="dark"
    )

    page = context.new_page()
    page.goto("https://www.saucedemo.com/")

    yield page

    context.close()


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
def logged_in_context(browser: Browser, playwright: Playwright):
    """Khởi tạo context nạp sẵn session đăng nhập từ data/state.json."""
    iphone_config = playwright.devices["iPhone 14 Pro Max"]
    storage_state_path = str(STATE_FILE) if STATE_FILE.exists() else None

    context_kwargs = {
        **iphone_config,
        "color_scheme": "dark"
    }
    if storage_state_path:
        context_kwargs["storage_state"] = storage_state_path

    context = browser.new_context(**context_kwargs)
    yield context
    context.close()


@pytest.fixture
def logged_in_page(logged_in_context):
    page = logged_in_context.new_page()
    yield page
    page.close()


@pytest.fixture
def logged_in_inventory_page(logged_in_page):
    logged_in_page.goto("https://www.saucedemo.com/inventory.html")
    return InventoryPage(logged_in_page)
