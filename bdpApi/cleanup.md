# Hướng dẫn dọn dẹp và tối ưu hóa mã nguồn

Sau khi phân tích mã nguồn, đây là danh sách các file và phần code có thể xóa hoặc tối ưu:

## 1. Các file có thể xóa

- `app/api/endpoints/camera.py` - Thay thế bằng model_service.py đã tối ưu hóa
- Thư mục `scripts/old/` - Chứa các file cũ không còn sử dụng
- Tất cả file `.pyc` và thư mục `__pycache__/`
- `app/templates/*.html` không cần thiết (giữ file index.html và 404.html)

## 2. Các phần code cần chỉnh sửa

### Trong `app/services/model_service.py`

- Xóa các model legacy không sử dụng
- Gộp các hàm trùng lặp
- Tối ưu hóa vòng lặp `_capture_loop`

### Trong `app/api/endpoints/websocket.py`

- Loại bỏ debug logs không cần thiết
- Tối ưu hóa xử lý lỗi
- Cải thiện quản lý kết nối WebSocket

### Trong `app/database/database.py`

- Tối ưu hóa các kết nối MongoDB
- Thêm pool kết nối
- Thêm xử lý lỗi chi tiết hơn

## 3. Cải thiện hiệu suất

- Thêm caching cho JWT token xác thực
- Sử dụng ThreadPoolExecutor để xử lý song song việc lưu ảnh
- Sử dụng GridFS cho MongoDB để lưu trữ ảnh hiệu quả hơn
- Tối ưu hóa MediaPipe Pose với chế độ GPU nếu có thể

## 4. Cải thiện bảo mật

- Thay đổi SECRET_KEY mặc định trong app/core/auth.py
- Thêm rate limiting cho API đăng nhập
- Sử dụng HTTPS cho ứng dụng production

## 5. Tối ưu hóa cấu trúc project

Cấu trúc project đề xuất sau khi dọn dẹp:

```
bdpApi/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── sessions.py
│   │   │   ├── labels.py
│   │   │   └── websocket.py
│   │   └── router.py
│   ├── core/
│   │   ├── auth.py
│   │   └── security.py
│   ├── database/
│   │   ├── database.py
│   │   └── init_db.py
│   ├── models/
│   │   ├── database_models.py
│   │   └── schemas.py
│   ├── services/
│   │   └── model_service.py
│   └── templates/
│       ├── index.html
│       └── 404.html
├── static/
│   └── css/
│       └── style.css
├── models/
│   ├── pose_classifier.h5
│   ├── leg_classifier.h5
│   ├── neck_classifier.h5
│   └── model_metadata.json
├── screenshots/
├── main.py
├── requirements.txt
└── README.md
```

## 6. Khởi động ứng dụng production 

Thay vì sử dụng uvicorn với `--reload` (chế độ phát triển), hãy sử dụng cấu hình production:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
``` 