import os
from pathlib import Path
import allure
import pytest
from playwright.sync_api import Page, expect

# Thư mục lưu file tạm phục vụ upload/download
TEMP_DIR = Path(__file__).parent.parent / "data"


# ==============================================================================
# KỸ NĂNG 1: XỬ LÝ MỞ TAB MỚI / CỬA SỔ POPUP (expect_popup)
# ==============================================================================
@allure.title("UI Phức tạp 1: Mở Tab mới (Popup) và chuyển ngữ cảnh")
def test_open_new_tab(page: Page):
    """
    Kịch bản: Mở trang có liên kết mở tab mới (target='_blank').
    Playwright sẽ lắng nghe sự kiện expect_popup() và tương tác trên tab mới.
    """
    page.goto("https://the-internet.herokuapp.com/windows")

    # Lắng nghe sự kiện mở tab mới trước khi thực hiện click
    with page.expect_popup() as popup_info:
        page.locator("a:has-text('Click Here')").click()

    # Nhận diện tab mới vừa bật lên
    new_tab = popup_info.value
    new_tab.wait_for_load_state()

    # Kiểm tra nội dung trên tab mới
    expect(new_tab.locator("h3")).to_have_text("New Window")
    assert "/windows/new" in new_tab.url

    # Đóng tab mới, quay lại tab chính làm việc tiếp
    new_tab.close()
    expect(page.locator("h3")).to_have_text("Opening a new window")


# ==============================================================================
# KỸ NĂNG 2: XỬ LÝ HỘP THOẠI DIALOG (Alert, Confirm, Prompt)
# Lưu ý: Mặc định Playwright tự động dismiss alert. Muốn accept hoặc đọc chữ
# ta phải đăng ký Event Listener 'page.on("dialog")' TRƯỚC KHI bấm nút.
# ==============================================================================
@allure.title("UI Phức tạp 2: Bắt và tương tác với JavaScript Alert Dialog")
def test_javascript_alerts(page: Page):
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")

    # Trường hợp 1: JS Confirm (Nhấn OK và kiểm tra thông điệp trên Alert)
    def handle_confirm(dialog):
        assert dialog.message == "I am a JS Confirm"
        dialog.accept()  # Bấm 'OK' (nếu muốn Cancel thì dùng dialog.dismiss())

    page.on("dialog", handle_confirm)
    page.locator("button:has-text('Click for JS Confirm')").click()
    expect(page.locator("#result")).to_have_text("You clicked: Ok")

    # Gỡ listener cũ để chuẩn bị cho test JS Prompt
    page.remove_listener("dialog", handle_confirm)

    # Trường hợp 2: JS Prompt (Nhập chữ vào hộp thoại rồi bấm OK)
    def handle_prompt(dialog):
        assert dialog.message == "I am a JS prompt"
        dialog.accept("Playwright Automation Test")  # Điền text vào prompt

    page.on("dialog", handle_prompt)
    page.locator("button:has-text('Click for JS Prompt')").click()
    expect(page.locator("#result")).to_have_text("You entered: Playwright Automation Test")


# ==============================================================================
# KỸ NĂNG 3: XỬ LÝ UPLOAD VÀ DOWNLOAD FILE
# Tuyệt chiêu: Không cần phụ thuộc vào hộp thoại Open File của hệ điều hành Windows!
# ==============================================================================
@allure.title("UI Phức tạp 3: Tải file lên (Upload) và Tải file về (Download)")
def test_upload_and_download(page: Page):
    # --- PHẦN 1: UPLOAD FILE ---
    page.goto("https://the-internet.herokuapp.com/upload")

    # Tạo một file txt tạm để upload
    sample_file = TEMP_DIR / "sample_upload.txt"
    sample_file.write_text("Hello Playwright Upload Test", encoding="utf-8")

    # Đưa đường dẫn file trực tiếp vào thẻ input file
    page.locator("#file-upload").set_input_files(str(sample_file))
    page.locator("#file-submit").click()

    # Kiểm tra thông báo upload thành công
    expect(page.locator("h3")).to_have_text("File Uploaded!")
    expect(page.locator("#uploaded-files")).to_contain_text("sample_upload.txt")

    # --- PHẦN 2: DOWNLOAD FILE ---
    page.goto("https://the-internet.herokuapp.com/download")

    # Lắng nghe sự kiện tải file trước khi click link tải
    with page.expect_download() as download_info:
        # Click vào file đầu tiên có trong danh sách
        page.locator(".example a").first.click()

    download = download_info.value

    # Lưu file đã tải về thư mục data/ của dự án
    downloaded_path = TEMP_DIR / download.suggested_filename
    download.save_as(str(downloaded_path))

    # Kiểm tra file đã thực sự tải về máy
    assert downloaded_path.exists()
    assert downloaded_path.stat().st_size > 0

    # Dọn dẹp các file tạm sau khi test xong
    if sample_file.exists():
        os.remove(sample_file)
    if downloaded_path.exists():
        os.remove(downloaded_path)


# ==============================================================================
# KỸ NĂNG 4: XỬ LÝ IFRAME (Khung nhúng)
# Tuyệt chiêu: Dùng page.frame_locator() để "xuyên thủng" Iframe
# ==============================================================================
@allure.title("UI Phức tạp 4: Thao tác bên trong khung Iframe")
def test_iframe_interaction(page: Page):
    page.goto("https://the-internet.herokuapp.com/iframe")

    # Xác định khung iframe của trình soạn thảo văn bản TinyMCE
    editor_frame = page.frame_locator("#mce_0_ifr")

    # Tìm phần tử body bên trong iframe và thao tác như bình thường
    editor_body = editor_frame.locator("#tinymce")

    # Xóa nội dung mặc định và gõ văn bản mới vào trong iframe
    editor_body.clear()
    editor_body.fill("Đây là văn bản được nhập tự động vào bên trong Iframe!")

    # Kiểm chứng nội dung đã hiển thị chính xác trong Iframe
    expect(editor_body).to_have_text("Đây là văn bản được nhập tự động vào bên trong Iframe!")
