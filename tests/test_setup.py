from pathlib import Path

# Xác định đường dẫn tuyệt đối đến thư mục data
DATA_PATH = Path(__file__).parent.parent / "data" / "state.json"

def test_save_login_state(login_page):
    """Đăng nhập 1 lần duy nhất để lưu lại trạng thái (Cookies/Session)"""
    
    # Bước 1: Sử dụng fixture login_page để đăng nhập (không cần khởi tạo browser thủ công)
    login_page.login("standard_user", "secret_sauce")
    
    # Bước 2: Đợi trang inventory tải xong để đảm bảo cookie/session đã được lưu đầy đủ
    login_page.page.wait_for_url("**/inventory.html")
    
    # Bước 3: Lưu trạng thái đăng nhập vào file state.json
    login_page.page.context.storage_state(path=str(DATA_PATH))