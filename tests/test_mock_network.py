import allure


@allure.title("Kiểm thử Mocking: Đánh chặn mạng, không cho tải hình ảnh")
def test_block_images_mocking(login_page, inventory_page):

    # 1. KÍCH HOẠT MOCKING: Lắng nghe toàn bộ request mạng
    # Bất cứ khi nào trình duyệt cố tải một file có đuôi png, jpg, jpeg hoặc svg,
    # Playwright sẽ can thiệp và hủy bỏ (abort) request đó ngay lập tức.
    login_page.page.route("**/*.{png,jpg,jpeg,svg}", lambda route: route.abort())

    # 2. THỰC HIỆN NGHIỆP VỤ: Đăng nhập như bình thường
    login_page.login("standard_user", "secret_sauce")

    # 3. KIỂM CHỨNG (ASSERTION)
    # Đảm bảo rằng dù không có hình ảnh, trang web không bị crash và vẫn load thành công
    assert inventory_page.is_inventory_displayed() == True

    # Đảm bảo khung dữ liệu của 6 sản phẩm vẫn được render đầy đủ trên màn hình
    assert inventory_page.get_items_count() == 6
