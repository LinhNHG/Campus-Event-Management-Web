# Hướng dẫn chạy bản giao diện mới

1. Giải nén ZIP vào một thư mục mới để giữ bản dự án cũ.
2. Mở PowerShell tại thư mục có `app.py`.
3. Chạy lần lượt:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

4. Mở http://127.0.0.1:5000 trong trình duyệt.
5. Đăng nhập bằng User ID `admin` để xem trang thống kê, quản lý sự kiện;
   hoặc `student1` để xem giao diện sinh viên. Luồng đăng nhập bằng User ID
   được giữ từ bản gốc.

## Những phần đã chỉnh

- Bố cục xanh đậm / mint thống nhất; thanh điều hướng bên trái trên desktop.
- Menu thu gọn, thẻ sự kiện một cột và biểu mẫu phù hợp trên điện thoại.
- Làm lại trang chủ, danh sách/chi tiết sự kiện, đăng ký, tài khoản, bảng và dashboard.
- Icon SVG, CSS và JavaScript nằm trong dự án, không cần CDN để hiển thị.
- Sửa dữ liệu trả về cho template và một số truy vấn thống kê không khớp schema.
- Giữ dữ liệu gốc. Các sự kiện mẫu có thể đã qua ngày hiện tại, nên Upcoming
  hiển thị 0; có thể tạo sự kiện mới hoặc sửa ngày để trình diễn.

Ảnh giao diện thật nằm trong thư mục `docs/`.
Bộ ZIP này chỉ là bản web, không thay thế file console Python của nhóm.
Đọc README.md để xem cấu trúc và hướng dẫn đưa code lên GitHub.
