# Body Detection Posture API (BDPAPI)

API phát hiện tư thế ngồi và cung cấp phản hồi thời gian thực thông qua WebSocket.

## Các tính năng

- Phát hiện tư thế ngồi sử dụng TensorFlow và MediaPipe
- Xác thực người dùng bằng JWT
- Giao tiếp thời gian thực qua WebSocket
- Lưu trữ dữ liệu phiên làm việc trong MongoDB
- Hỗ trợ cả camera local và camera WiFi

## Cài đặt

### Yêu cầu

- Python 3.8+
- MongoDB đã cài đặt và đang chạy
- Camera (webcam hoặc camera IP)

### Các bước cài đặt

1. **Clone repository**

2. **Cài đặt thư viện phụ thuộc**
   ```bash
   cd bdpApi
   pip install -r requirements.txt
   ```

3. **Cấu hình database**
   
   Mở file `app/config.py` và cập nhật cấu hình MongoDB nếu cần:
   ```python
   MONGODB_URL = "mongodb://localhost:27017"
   DB_NAME = "detection_system"
   ```

4. **Khởi tạo database**
   ```bash
   python -m app.database.init_db
   ```

5. **Khởi động server**
   ```bash
   uvicorn main:app --reload
   ```

## Sử dụng API với Postman

### 1. Đăng ký người dùng mới

- **Method**: POST
- **URL**: `http://localhost:8000/api/auth/register`
- **Body**: raw JSON
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "test123"
}
```

### 2. Lấy JWT Token 

#### Cách 1: Đăng nhập với username/password
- **Method**: POST
- **URL**: `http://localhost:8000/api/auth/token`
- **Body**: x-www-form-urlencoded
  - Key: `username`, Value: `testuser`
  - Key: `password`, Value: `test123`

#### Cách 2: Lấy token với user_id
- **Method**: POST
- **URL**: `http://localhost:8000/api/auth/user-token`
- **Body**: raw JSON
```json
{
  "user_id": "your_mongodb_user_id"
}
```

### 3. Kết nối WebSocket và phát hiện tư thế

1. **Tạo WebSocket request trong Postman**
   - Click "New" > "WebSocket Request"

2. **Kết nối WebSocket**
   - URL: `ws://localhost:8000/api/ws?client_id=test123&token=YOUR_JWT_TOKEN`
   - Click "Connect"

3. **Bắt đầu phát hiện tư thế với webcam**
   - Gửi JSON message:
   ```json
   {
     "action": "start",
     "camera_id": 0
   }
   ```

4. **Bắt đầu phát hiện tư thế với camera WiFi**
   - Gửi JSON message:
   ```json
   {
     "action": "start",
     "camera_id": 1,
     "camera_url": "http://192.168.1.10:8080/video"
   }
   ```

5. **Dừng phát hiện tư thế**
   - Gửi JSON message:
   ```json
   {
     "action": "stop"
   }
   ```

## Các loại tin nhắn WebSocket

### Tin nhắn nhận từ server:

1. **Kết quả phát hiện tư thế**
   ```json
   {
     "type": "detection_result",
     "data": {
       "image": "base64_encoded_image",
       "posture": {
         "posture": "good_posture",
         "confidence": 0.95,
         "need_alert": false
       },
       "timestamp": "2023-04-28T15:30:45.123456",
       "image_path": "/path/to/image.jpg",
       "is_new_posture": true,
       "duration": 0
     }
   }
   ```

2. **Cập nhật tư thế (không kèm hình ảnh)**
   ```json
   {
     "type": "posture_update",
     "data": {
       "posture": {
         "posture": "good_posture",
         "confidence": 0.95,
         "need_alert": false
       },
       "timestamp": "2023-04-28T15:30:45.123456",
       "duration": 10.5
     }
   }
   ```

3. **Thông báo hoàn tất session item**
   ```json
   {
     "type": "session_item_completed",
     "data": {
       "session_item_id": "mongodb_id",
       "label_id": "good_posture",
       "start_time": "2023-04-28T15:30:45.123456",
       "end_time": "2023-04-28T15:31:45.123456",
       "duration_seconds": 60.0
     }
   }
   ```

## Tối ưu hóa và xử lý lỗi

1. **Xử lý lỗi kết nối camera**
   - Hệ thống tự động thử kết nối lại tối đa 5 lần nếu mất kết nối với camera WiFi
   - Thông báo rõ ràng nếu không thể kết nối

2. **Tối ưu lưu trữ và truyền dữ liệu**
   - Ảnh chỉ được lưu và gửi khi phát hiện tư thế mới hoặc sau mỗi 2 giây
   - Gửi dữ liệu nhẹ không kèm ảnh trong các cập nhật trung gian

3. **Xác thực và bảo mật**
   - JWT authentication để bảo vệ API
   - Mật khẩu được mã hóa bằng bcrypt

## Cấu trúc cơ sở dữ liệu

- **users**: Thông tin người dùng
- **sessions**: Các phiên làm việc
- **session_items**: Chi tiết từng tư thế trong một phiên
- **labels**: Các nhãn tư thế và khuyến nghị

## Cấu trúc mã nguồn

- **app/**
  - **api/**: Các API endpoints
  - **core/**: Xác thực và bảo mật
  - **database/**: Kết nối và truy vấn MongoDB
  - **models/**: Schemas và database models
  - **services/**: Dịch vụ phát hiện tư thế
  - **templates/**: Templates HTML
- **static/**: Tài nguyên tĩnh
- **main.py**: Điểm khởi chạy ứng dụng 