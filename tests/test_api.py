import allure
import pytest
from playwright.sync_api import Playwright, APIRequestContext, expect


# --------------------------------------------------------------------------
# FIXTURE KHỞI TẠO API REQUEST CONTEXT
# Không cần mở trình duyệt, gửi HTTP Request trực tiếp qua Playwright engine
# --------------------------------------------------------------------------
@pytest.fixture(scope="session")
def api_client(playwright: Playwright) -> APIRequestContext:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=UTF-8",
    }
    # Khởi tạo ngữ cảnh gọi API với Base URL chuẩn
    context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com",
        extra_http_headers=headers
    )
    yield context
    # Dọn dẹp và giải phóng tài nguyên sau khi chạy xong
    context.dispose()


class TestAPIAutomation:
    """Bộ kiểm thử RESTful API bằng Playwright APIRequestContext."""

    @allure.title("API 1: [GET] Lấy chi tiết bài viết và kiểm tra dữ liệu")
    def test_get_post_detail(self, api_client: APIRequestContext):
        # 1. Gửi request GET tới /posts/1
        response = api_client.get("/posts/1")

        # 2. Kiểm chứng HTTP Status Code phải là 200 OK
        assert response.status == 200, f"Expected 200 but got {response.status}"
        assert response.ok  # Tương đương assert 200 <= status < 300

        # 3. Đọc dữ liệu JSON trả về
        data = response.json()

        # 4. Kiểm chứng cấu trúc dữ liệu và giá trị mong đợi
        assert data["id"] == 1
        assert data["userId"] == 1
        assert len(data["title"]) > 0
        assert "sunt aut facere" in data["title"]

    @allure.title("API 2: [POST] Tạo một bài viết mới (Create Post)")
    def test_create_new_post(self, api_client: APIRequestContext):
        # Dữ liệu payload cần gửi lên server
        payload = {
            "title": "Học Playwright API Testing",
            "body": "Playwright hỗ trợ kiểm thử API siêu nhanh và mạnh mẽ!",
            "userId": 99
        }

        # 1. Gửi request POST kèm data JSON
        response = api_client.post("/posts", data=payload)

        # 2. Kiểm chứng Status Code khi tạo mới thành công là 201 Created
        assert response.status == 201

        # 3. Kiểm tra dữ liệu phản hồi từ server
        created_data = response.json()
        assert created_data["title"] == payload["title"]
        assert created_data["body"] == payload["body"]
        assert created_data["userId"] == payload["userId"]
        assert "id" in created_data  # Server phải tự sinh ra trường ID mới

    @allure.title("API 3: [PUT] Cập nhật thông tin bài viết (Update Post)")
    def test_update_post(self, api_client: APIRequestContext):
        update_payload = {
            "id": 1,
            "title": "Tiêu đề đã được cập nhật qua Playwright",
            "body": "Nội dung mới sau khi sửa",
            "userId": 1
        }

        # 1. Gửi request PUT để sửa bài viết số 1
        response = api_client.put("/posts/1", data=update_payload)

        assert response.status == 200
        result = response.json()
        assert result["title"] == update_payload["title"]

    @allure.title("API 4: [DELETE] Xóa một bài viết (Delete Post)")
    def test_delete_post(self, api_client: APIRequestContext):
        # 1. Gửi request DELETE tới bài viết số 1
        response = api_client.delete("/posts/1")

        # 2. Kiểm chứng kết quả thành công
        assert response.status == 200
