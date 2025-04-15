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


## API Thống kê tư thế

API thống kê cung cấp dữ liệu phân tích chi tiết về tư thế của người dùng theo nhiều khía cạnh khác nhau, giúp hiển thị biểu đồ và báo cáo trực quan.

### 1. Phân bố tư thế

- **Method**: GET
- **URL**: `/api/analytics/distribution`
- **Query Parameters**:
  - `start_date`: Thời gian bắt đầu (tùy chọn)
  - `end_date`: Thời gian kết thúc (tùy chọn)
  - `session_id`: ID phiên cụ thể (tùy chọn)
- **Response**: Phân bố các loại tư thế, bao gồm số lượng, thời lượng và phần trăm

### 2. Thời lượng tư thế

- **Method**: GET
- **URL**: `/api/analytics/duration`
- **Query Parameters**:
  - `start_date`: Thời gian bắt đầu (tùy chọn)
  - `end_date`: Thời gian kết thúc (tùy chọn)
  - `session_id`: ID phiên cụ thể (tùy chọn)
- **Response**: Thời lượng của mỗi loại tư thế, bao gồm tổng thời gian, thời gian trung bình, tối đa, tối thiểu

### 3. Lịch sử tư thế

- **Method**: GET
- **URL**: `/api/analytics/history`
- **Query Parameters**:
  - `start_date`: Thời gian bắt đầu (tùy chọn)
  - `end_date`: Thời gian kết thúc (tùy chọn)
  - `limit`: Số lượng mục tối đa (mặc định: 100)
- **Response**: Lịch sử chi tiết các tư thế theo thời gian

### 4. Sự cải thiện tư thế

- **Method**: GET
- **URL**: `/api/analytics/improvement`
- **Query Parameters**:
  - `days`: Số ngày phân tích (mặc định: 30)
- **Response**: Dữ liệu về sự cải thiện tư thế theo thời gian, xu hướng tư thế tốt/xấu

### 5. Tóm tắt tư thế theo ngày

- **Method**: GET
- **URL**: `/api/analytics/daily-summary`
- **Query Parameters**:
  - `date`: Ngày cần phân tích (mặc định: ngày hiện tại)
- **Response**: Tóm tắt chi tiết tư thế trong một ngày, bao gồm phân bố theo giờ

### 6. Tóm tắt tư thế theo tuần

- **Method**: GET
- **URL**: `/api/analytics/weekly-summary`
- **Query Parameters**:
  - `start_date`: Ngày đầu tuần (mặc định: thứ 2 của tuần hiện tại)
- **Response**: Tóm tắt chi tiết tư thế trong một tuần, bao gồm phân bố theo ngày

### 7. So sánh hai khoảng thời gian

- **Method**: GET
- **URL**: `/api/analytics/compare-periods`
- **Query Parameters**:
  - `period1_start`: Thời gian bắt đầu khoảng 1
  - `period1_end`: Thời gian kết thúc khoảng 1
  - `period2_start`: Thời gian bắt đầu khoảng 2
  - `period2_end`: Thời gian kết thúc khoảng 2
- **Response**: So sánh chi tiết về tư thế giữa hai khoảng thời gian

### 8. Thống kê tổng hợp người dùng

- **Method**: GET
- **URL**: `/api/analytics/user-stats`
- **Response**: Thống kê tổng hợp về người dùng, bao gồm tổng số phiên, thời gian sử dụng, tỷ lệ tư thế tốt/xấu

## Dữ liệu biểu đồ

API thống kê cung cấp dữ liệu phù hợp cho các loại biểu đồ sau:

1. **Biểu đồ tròn**: Sử dụng dữ liệu từ `/api/analytics/distribution` để hiển thị phân bố tư thế
2. **Biểu đồ cột**: Sử dụng dữ liệu từ `/api/analytics/duration` để hiển thị thời lượng các tư thế
3. **Biểu đồ đường**: Sử dụng dữ liệu từ `/api/analytics/improvement` để hiển thị xu hướng tư thế theo thời gian
4. **Biểu đồ nhiệt**: Sử dụng dữ liệu từ `/api/analytics/daily-summary` để hiển thị phân bố tư thế theo giờ
5. **Biểu đồ so sánh**: Sử dụng dữ liệu từ `/api/analytics/compare-periods` để so sánh hai khoảng thời gian


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