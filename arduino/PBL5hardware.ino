#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>
#include "DFRobotDFPlayerMini.h"

// FreeRTOS includes
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/semphr.h"

// ===================
// Select camera model
// ===================
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

// WiFi credentials
const char* ssid = "Thu Nam";
const char* password = "thunam12345";

// Sử dụng Hardware Serial cho DFPlayer
HardwareSerial mySerial(1); // Sử dụng UART1 (GPIO14 và GPIO15)

// DFPlayer object
DFRobotDFPlayerMini player;

// Tạo 2 web server trên các port khác nhau
WebServer serverCamera(80);    // Camera server trên port 80
WebServer serverSpeaker(81);   // Speaker server trên port 81

// Semaphores và Mutexes để đồng bộ hóa các task
SemaphoreHandle_t dfPlayerMutex;
SemaphoreHandle_t cameraMutex;

// Cấu trúc để truyền thông tin giữa các task
struct DFPlayerCommand {
  int command;  // 1=play, 2=volume, 3=pause, 4=resume, 5=next, 6=prev
  int value;    // track number or volume level
};

// Queue để gửi lệnh từ task web đến task DFPlayer
QueueHandle_t dfPlayerQueue;

// Task handles
TaskHandle_t cameraTaskHandle = NULL;
TaskHandle_t speakerTaskHandle = NULL;
TaskHandle_t webServerTaskHandle = NULL;
TaskHandle_t streamingTaskHandle = NULL;  // Thêm task handle cho streaming
TaskHandle_t watchdogTaskHandle = NULL;   // Thêm watchdog task

// Biến cờ để kiểm soát các client stream
bool clientsStreaming = false;
WiFiClient streamingClient;  // Client cho streaming
bool hasStreamingClient = false;  // Cờ để kiểm tra có client streaming không

// Biến cho streaming monitoring
volatile unsigned long lastStreamingActivity = 0;
volatile unsigned long streamingStartTime = 0;
volatile bool streamingHealthy = true;

// Task xử lý streaming riêng biệt
void streamingTask(void * parameter) {
  TickType_t lastFrameTime = 0;
  const TickType_t frameTimeout = pdMS_TO_TICKS(5000); // 5 giây timeout
  
  while(true) {
    if (hasStreamingClient && streamingClient.connected()) {
      // Kiểm tra timeout - nếu quá lâu không gửi frame thì reset connection
      if (xTaskGetTickCount() - lastFrameTime > frameTimeout && lastFrameTime != 0) {
        Serial.println("Streaming timeout, resetting connection...");
        hasStreamingClient = false;
        clientsStreaming = false;
        streamingClient.stop();
        vTaskDelay(100 / portTICK_PERIOD_MS);
        continue;
      }
      
      // Thử lấy mutex với timeout ngắn để tránh blocking
      if (xSemaphoreTake(cameraMutex, 200 / portTICK_PERIOD_MS) == pdTRUE) {
        camera_fb_t * fb = esp_camera_fb_get();
        if (fb) {
          // Kiểm tra kích thước frame hợp lệ
          if (fb->len > 0 && fb->len < 100000) { // Giới hạn kích thước hợp lý
            // Kiểm tra client vẫn connected trước khi gửi
            if (streamingClient.connected()) {
              size_t bytesWritten = 0;
              
              // Gửi boundary và headers
              bytesWritten += streamingClient.println();
              bytesWritten += streamingClient.println("--frame");
              bytesWritten += streamingClient.print("Content-Type: image/jpeg\r\n");
              bytesWritten += streamingClient.print("Content-Length: ");
              bytesWritten += streamingClient.print(fb->len);
              bytesWritten += streamingClient.print("\r\n\r\n");
              
              // Gửi dữ liệu hình ảnh trong chunks nhỏ để tránh buffer overflow
              const size_t chunkSize = 1024;
              uint8_t* buffer = fb->buf;
              size_t remaining = fb->len;
              size_t sent = 0;
              
              while (remaining > 0 && streamingClient.connected()) {
                size_t toSend = (remaining > chunkSize) ? chunkSize : remaining;
                size_t actualSent = streamingClient.write(buffer + sent, toSend);
                
                if (actualSent == 0) {
                  Serial.println("Failed to send chunk, connection may be lost");
                  break;
                }
                
                sent += actualSent;
                remaining -= actualSent;
                
                // Nhỏ delay giữa các chunks
                if (remaining > 0) {
                  vTaskDelay(1 / portTICK_PERIOD_MS);
                }
              }
              
              if (remaining == 0) {
                streamingClient.println();
                lastFrameTime = xTaskGetTickCount();
              } else {
                Serial.println("Failed to send complete frame");
              }
            } else {
              Serial.println("Client disconnected during frame send");
              hasStreamingClient = false;
              clientsStreaming = false;
            }
          } else {
            Serial.printf("Invalid frame size: %d bytes\n", fb->len);
          }
          
          esp_camera_fb_return(fb);
        } else {
          Serial.println("Failed to capture frame");
          vTaskDelay(100 / portTICK_PERIOD_MS); // Delay khi lỗi
        }
        xSemaphoreGive(cameraMutex);
      } else {
        Serial.println("Failed to take camera mutex, skipping frame");
      }
      
      // Điều chỉnh frame rate - 15 FPS thay vì 30 FPS để ổn định hơn
      vTaskDelay(50 / portTICK_PERIOD_MS); // ~15 FPS
    } else {
      // Nếu không có client hoặc client đã ngắt kết nối
      if (hasStreamingClient) {
        Serial.println("Client disconnected, cleaning up...");
        hasStreamingClient = false;
        clientsStreaming = false;
        streamingClient.stop();
        lastFrameTime = 0;
      }
      vTaskDelay(100 / portTICK_PERIOD_MS);
    }
    
    // Yield cho các task khác
    taskYIELD();
  }
}

// Task xử lý camera streaming (đã sửa đổi)
void cameraStreamTask(void * parameter) {
  while(true) {
    if (clientsStreaming) {
      // Chỉ xử lý khi có client đang stream
      vTaskDelay(10 / portTICK_PERIOD_MS); // Nhường CPU cho các task khác
    } else {
      vTaskDelay(100 / portTICK_PERIOD_MS); // Khi không có client, ngủ lâu hơn
    }
  }
}

// Task xử lý DFPlayer
void dfPlayerTask(void * parameter) {
  DFPlayerCommand cmd;
  
  while(true) {
    // Đợi lệnh từ queue
    if (xQueueReceive(dfPlayerQueue, &cmd, portMAX_DELAY) == pdTRUE) {
      // Lấy mutex trước khi truy cập DFPlayer
      if (xSemaphoreTake(dfPlayerMutex, portMAX_DELAY) == pdTRUE) {
        switch (cmd.command) {
          case 1: // play
            player.play(cmd.value);
            break;
          case 2: // volume
            player.volume(cmd.value);
            break;
          case 3: // pause
            player.pause();
            break;
          case 4: // resume
            player.start();
            break;
          case 5: // next
            player.next();
            break;
          case 6: // prev
            player.previous();
            break;
        }
        
        // Giải phóng mutex sau khi hoàn thành
        xSemaphoreGive(dfPlayerMutex);
      }
    }
    
    // Kiểm tra và xử lý trạng thái DFPlayer
    if (xSemaphoreTake(dfPlayerMutex, 0) == pdTRUE) {
      if (player.available()) {
        uint8_t type = player.readType();
        int value = player.read();
        
        // Xử lý thông báo từ DFPlayer (chỉ ghi log)
        if (type == DFPlayerError) {
          Serial.print(F("DFPlayerError:"));
          switch (value) {
            case Busy:
              Serial.println(F("Card not found"));
              break;
            case Sleeping:
              Serial.println(F("Sleeping"));
              break;
            case SerialWrongStack:
              Serial.println(F("Get Wrong Stack"));
              break;
            case CheckSumNotMatch:
              Serial.println(F("Check Sum Not Match"));
              break;
            case FileIndexOut:
              Serial.println(F("File Index Out of Bound"));
              break;
            case FileMismatch:
              Serial.println(F("Cannot Find File"));
              break;
            case Advertise:
              Serial.println(F("In Advertise"));
              break;
            default:
              break;
          }
        }
      }
      xSemaphoreGive(dfPlayerMutex);
    }
    
    vTaskDelay(50 / portTICK_PERIOD_MS);
  }
}

// Task xử lý web server
void webServerTask(void * parameter) {
  while(true) {
    // Xử lý các yêu cầu từ cả hai server
    serverCamera.handleClient();
    serverSpeaker.handleClient();
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

// Hàm xử lý streaming (đã sửa đổi để không blocking)
void handleMjpegStream() {
  // Nếu đã có client streaming, từ chối client mới
  if (hasStreamingClient) {
    serverCamera.send(503, "text/plain", "Streaming busy - only one client allowed");
    Serial.println("Rejected new client - streaming busy");
    return;
  }
  
  WiFiClient client = serverCamera.client();
  
  // Kiểm tra client connection
  if (!client || !client.connected()) {
    Serial.println("Invalid client connection");
    serverCamera.send(400, "text/plain", "Invalid connection");
    return;
  }
  
  Serial.println("New streaming client connected");
  
  // Gửi header cho MJPEG stream với timeout
  client.setTimeout(10000); // 10 giây timeout
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: multipart/x-mixed-replace; boundary=frame");
  client.println("Cache-Control: no-cache, no-store, max-age=0, must-revalidate");
  client.println("Pragma: no-cache");
  client.println("Expires: Thu, 01 Dec 1994 16:00:00 GMT");
  client.println("Connection: close");
  client.println();
  
  // Lưu client và đánh dấu đang streaming
  streamingClient = client;
  hasStreamingClient = true;
  clientsStreaming = true;
  
  Serial.println("Streaming started successfully");
  
  // Không cần vòng lặp blocking ở đây nữa
  // Task streamingTask sẽ xử lý việc gửi frame
}

// Hàm xử lý chụp ảnh
void handleCapturePhoto() {
  if (xSemaphoreTake(cameraMutex, portMAX_DELAY) == pdTRUE) {
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
      xSemaphoreGive(cameraMutex);
      serverCamera.send(500, "text/plain", "Camera capture failed");
      return;
    }
    
    serverCamera.setContentLength(fb->len);
    serverCamera.sendHeader("Content-Type", "image/jpeg");
    serverCamera.sendHeader("Content-Disposition", "attachment; filename=capture.jpg");
    serverCamera.send(200);
    
    WiFiClient client = serverCamera.client();
    client.write(fb->buf, fb->len);
    
    esp_camera_fb_return(fb);
    xSemaphoreGive(cameraMutex);
  }
}

void setupCameraServer() {
  // Trang chủ với giao diện người dùng
  serverCamera.on("/", HTTP_GET, []() {
    String html = "<html><head><title>ESP32-CAM Stream</title>";
    html += "<meta name='viewport' content='width=device-width, initial-scale=1'>";
    html += "<style>";
    html += "body { font-family: Arial; text-align: center; margin: 20px; background-color: #f0f0f0; }";
    html += ".container { max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }";
    html += "h1 { color: #2c3e50; }";
    html += "img { width: 100%; max-width: 640px; border-radius: 8px; margin: 10px 0; }";
    html += "a { display: inline-block; background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 15px; }";
    html += ".controls { margin: 15px 0; }";
    html += "button { background-color: #2ecc71; color: white; border: none; padding: 8px 15px; margin: 5px; border-radius: 4px; cursor: pointer; }";
    html += "button:hover { background-color: #27ae60; }";
    html += "</style>";
    
    // Script để tự động làm mới hình ảnh
    html += "<script>";
    html += "let streaming = false;";
    html += "function toggleStream() {";
    html += "  const img = document.getElementById('stream');";
    html += "  const btn = document.getElementById('streamBtn');";
    html += "  if (streaming) {";
    html += "    img.src = '';";
    html += "    fetch('/stop_stream');";  // Gọi endpoint để dừng streaming
    html += "    btn.innerHTML = 'Bắt đầu Stream';";
    html += "    streaming = false;";
    html += "  } else {";
    html += "    img.src = '/stream';";
    html += "    btn.innerHTML = 'Dừng Stream';";
    html += "    streaming = true;";
    html += "  }";
    html += "}";
    
    // Thêm chức năng chụp ảnh
    html += "function capturePhoto() {";
    html += "  fetch('/capture')";
    html += "    .then(response => response.blob())";
    html += "    .then(blob => {";
    html += "      const url = URL.createObjectURL(blob);";
    html += "      const a = document.createElement('a');";
    html += "      a.href = url;";
    html += "      a.download = 'capture.jpg';";
    html += "      a.click();";
    html += "    });";
    html += "}";
    html += "</script>";
    html += "</head><body>";
    
    html += "<div class='container'>";
    html += "<h1>ESP32-CAM Camera Stream</h1>";
    html += "<img id='stream' src='' alt='Camera Stream'>";
    
    html += "<div class='controls'>";
    html += "<button id='streamBtn' onclick='toggleStream()'>Bắt đầu Stream</button>";
    html += "<button onclick='capturePhoto()'>Chụp ảnh</button>";
    html += "</div>";
    
    html += "<a href='http://" + WiFi.localIP().toString() + ":81'>Điều khiển Loa</a>";
    html += "</div></body></html>";
    
    serverCamera.send(200, "text/html", html);
  });

  // Endpoint để chụp ảnh
  serverCamera.on("/capture", HTTP_GET, handleCapturePhoto);

  // Endpoint MJPEG streaming
  serverCamera.on("/stream", HTTP_GET, handleMjpegStream);

  // Endpoint để dừng streaming
  serverCamera.on("/stop_stream", HTTP_GET, []() {
    if (hasStreamingClient) {
      hasStreamingClient = false;
      clientsStreaming = false;
      streamingClient.stop();
    }
    serverCamera.send(200, "text/plain", "Stream stopped");
  });

  serverCamera.begin();
}

void startSpeakerServer() {
  serverSpeaker.on("/", HTTP_GET, []() {
    String html = "<html><head><title>ESP32-CAM DFPlayer</title>";
    html += "<meta name='viewport' content='width=device-width, initial-scale=1'>";
    html += "<style>";
    html += "body { font-family: Arial; text-align: center; margin: 20px; background-color: #f0f0f0; }";
    html += ".container { max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }";
    html += "h1 { color: #2c3e50; }";
    html += "h2 { color: #3498db; margin-top: 20px; }";
    html += "button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin: 5px; cursor: pointer; }";
    html += "button:hover { background-color: #45a049; }";
    html += "input { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }";
    html += ".control-section { background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin: 15px 0; }";
    html += "a { display: inline-block; background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 15px; }";
    html += "</style></head><body>";
    
    html += "<div class='container'>";
    html += "<h1>ESP32-CAM DFPlayer Control</h1>";
    html += "<a href='http://" + WiFi.localIP().toString() + "'>Xem Camera</a>";
    
    html += "<div class='control-section'>";
    html += "<h2>Phát nhạc</h2>";
    html += "<form action='/play'>";
    html += "Số bài: <input type='number' name='track' min='1' max='100' value='1'>";
    html += "<input type='submit' value='Phát' style='background-color: #4CAF50; color: white;'>";
    html += "</form></div>";

    html += "<div class='control-section'>";
    html += "<h2>Âm lượng</h2>";
    html += "<form action='/volume'>";
    html += "Mức (0-30): <input type='number' name='vol' min='0' max='30' value='20'>";
    html += "<input type='submit' value='Đặt' style='background-color: #4CAF50; color: white;'>";
    html += "</form></div>";

    html += "<div class='control-section'>";
    html += "<h2>Điều khiển</h2>";
    html += "<button onclick='location.href=\"/pause\"'>Tạm dừng</button>";
    html += "<button onclick='location.href=\"/resume\"'>Tiếp tục</button>";
    html += "<button onclick='location.href=\"/next\"'>Bài tiếp</button>";
    html += "<button onclick='location.href=\"/prev\"'>Bài trước</button>";
    html += "</div>";

    html += "</div></body></html>";
    serverSpeaker.send(200, "text/html", html);
  });

  // Thay vì trực tiếp điều khiển DFPlayer, gửi lệnh qua queue
  serverSpeaker.on("/play", HTTP_GET, []() {
    String trackStr = serverSpeaker.arg("track");
    if (trackStr != "") {
      int track = trackStr.toInt();
      DFPlayerCommand cmd = {1, track}; // command=1 (play), value=track number
      xQueueSend(dfPlayerQueue, &cmd, portMAX_DELAY);
    }
    serverSpeaker.sendHeader("Location", "/", true);
    serverSpeaker.send(302, "text/plain", "");
  });

  serverSpeaker.on("/volume", HTTP_GET, []() {
    String volStr = serverSpeaker.arg("vol");
    if (volStr != "") {
      int vol = volStr.toInt();
      if (vol >= 0 && vol <= 30) {
        DFPlayerCommand cmd = {2, vol}; // command=2 (volume), value=volume level
        xQueueSend(dfPlayerQueue, &cmd, portMAX_DELAY);
      }
    }
    serverSpeaker.sendHeader("Location", "/", true);
    serverSpeaker.send(302, "text/plain", "");
  });

  serverSpeaker.on("/pause", HTTP_GET, []() {
    DFPlayerCommand cmd = {3, 0}; // command=3 (pause), value=0 (not used)
    xQueueSend(dfPlayerQueue, &cmd, portMAX_DELAY);
    serverSpeaker.sendHeader("Location", "/", true);
    serverSpeaker.send(302, "text/plain", "");
  });

  serverSpeaker.on("/resume", HTTP_GET, []() {
    DFPlayerCommand cmd = {4, 0}; // command=4 (resume), value=0 (not used)
    xQueueSend(dfPlayerQueue, &cmd, portMAX_DELAY);
    serverSpeaker.sendHeader("Location", "/", true);
    serverSpeaker.send(302, "text/plain", "");
  });

  serverSpeaker.on("/next", HTTP_GET, []() {
    DFPlayerCommand cmd = {5, 0}; // command=5 (next), value=0 (not used)
    xQueueSend(dfPlayerQueue, &cmd, portMAX_DELAY);
    serverSpeaker.sendHeader("Location", "/", true);
    serverSpeaker.send(302, "text/plain", "");
  });

  serverSpeaker.on("/prev", HTTP_GET, []() {
    DFPlayerCommand cmd = {6, 0}; // command=6 (prev), value=0 (not used)
    xQueueSend(dfPlayerQueue, &cmd, portMAX_DELAY);
    serverSpeaker.sendHeader("Location", "/", true);
    serverSpeaker.send(302, "text/plain", "");
  });

  serverSpeaker.begin();
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // Khởi tạo các semaphore và mutex
  dfPlayerMutex = xSemaphoreCreateMutex();
  cameraMutex = xSemaphoreCreateMutex();
  
  // Khởi tạo queue cho lệnh DFPlayer
  dfPlayerQueue = xQueueCreate(10, sizeof(DFPlayerCommand));

  // Khởi tạo camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_VGA;  // Cân bằng giữa chất lượng và tốc độ khung hình
  config.pixel_format = PIXFORMAT_JPEG;
  config.grab_mode = CAMERA_GRAB_LATEST;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 2;

  // Cấu hình camera dựa trên PSRAM
  if(config.pixel_format == PIXFORMAT_JPEG){
    if(psramFound()){
      config.jpeg_quality = 10;
      config.fb_count = 2;
      config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
      config.frame_size = FRAMESIZE_SVGA;
      config.fb_location = CAMERA_FB_IN_DRAM;
    }
  } else {
    config.frame_size = FRAMESIZE_240X240;
  }

  // Khởi tạo camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // Cấu hình thêm cho sensor
  sensor_t * s = esp_camera_sensor_get();
  if (s) {
    // Tăng tốc độ khung hình bằng cách giảm độ phân giải
    s->set_framesize(s, FRAMESIZE_VGA);  // 640x480 - cân bằng giữa chất lượng và tốc độ
    
    // Sửa camera bị ngược upside down
    s->set_vflip(s, 1);       // Flip theo chiều dọc (vertical flip) - sửa upside down
    // s->set_hmirror(s, 1);     // Mirror theo chiều ngang (horizontal mirror) - tùy chọn
    
    // Tối ưu hóa chất lượng hình ảnh
    s->set_quality(s, 10);  // 10-63, thấp hơn = chất lượng cao hơn
    s->set_brightness(s, 1);  // -2 to 2
    s->set_contrast(s, 1);    // -2 to 2
    s->set_saturation(s, 1);  // -2 to 2
    s->set_sharpness(s, 1);   // -2 to 2
    s->set_denoise(s, 1);     // 0 to 1
    
    // Các cài đặt khác
    s->set_whitebal(s, 1);    // 0 = disable, 1 = enable
    s->set_awb_gain(s, 1);    // 0 = disable, 1 = enable
    s->set_wb_mode(s, 0);     // 0 to 4
    s->set_exposure_ctrl(s, 1);  // 0 = disable, 1 = enable
    s->set_aec2(s, 1);           // 0 = disable, 1 = enable
    s->set_gain_ctrl(s, 1);      // 0 = disable, 1 = enable
    s->set_special_effect(s, 0); // 0 = No Effect
  }

  // Khởi tạo Serial1 cho DFPlayer
  mySerial.begin(9600, SERIAL_8N1, 14, 15); // RX=GPIO14, TX=GPIO15
  Serial.println("Đang kết nối DFPlayer...");
  
  // Thử kết nối với DFPlayer
  if (!player.begin(mySerial)) {
    Serial.println("Không thể kết nối với DFPlayer!");
    Serial.println("1) Kiểm tra lại dây nối");
    Serial.println("2) Kiểm tra thẻ nhớ");
  } else {
    Serial.println("DFPlayer Mini đã kết nối!");

    // Cấu hình DFPlayer
    player.setTimeOut(500);
    player.volume(20);
    player.EQ(DFPLAYER_EQ_NORMAL);
    player.outputDevice(DFPLAYER_DEVICE_SD);
  }

  // Kết nối WiFi
  WiFi.begin(ssid, password);
  Serial.print("Đang kết nối WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nĐã kết nối WiFi!");
  Serial.print("Camera URL: http://");
  Serial.println(WiFi.localIP());
  Serial.print("Speaker URL: http://");
  Serial.print(WiFi.localIP());
  Serial.println(":81");

  // Khởi động cả hai server
  setupCameraServer();
  startSpeakerServer();
  
  // Tạo các task
  xTaskCreatePinnedToCore(
    webServerTask,          // Task function
    "WebServerTask",        // Task name
    8192,                   // Stack size (bytes)
    NULL,                   // Parameter
    1,                      // Task priority
    &webServerTaskHandle,   // Task handle
    0                       // Core ID (0)
  );
  
  xTaskCreatePinnedToCore(
    dfPlayerTask,           // Task function
    "DFPlayerTask",         // Task name
    4096,                   // Stack size (bytes)
    NULL,                   // Parameter
    2,                      // Task priority
    &speakerTaskHandle,     // Task handle
    1                       // Core ID (1)
  );
  
  xTaskCreatePinnedToCore(
    cameraStreamTask,       // Task function
    "CameraStreamTask",     // Task name
    4096,                   // Stack size (bytes)
    NULL,                   // Parameter
    2,                      // Task priority
    &cameraTaskHandle,      // Task handle
    1                       // Core ID (1)
  );
  
  xTaskCreatePinnedToCore(
    streamingTask,          // Task function
    "StreamingTask",        // Task name
    8192,                   // Stack size (bytes)
    NULL,                   // Parameter
    3,                      // Task priority (cao hơn để ưu tiên streaming)
    &streamingTaskHandle,   // Task handle
    1                       // Core ID (1)
  );
  
  Serial.println("Tất cả các task đã được khởi tạo");
}

void loop() {
  // Vòng lặp chính không làm gì cả vì tất cả công việc được xử lý trong các task
  vTaskDelay(1000 / portTICK_PERIOD_MS);
}
