import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from components.button import ButtonFactory
from _config.theme import Theme
from utils.model_loader import load_model_and_encoder
import mediapipe as mp
import numpy as np  # Import numpy

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

class OwnCamera(ctk.CTkFrame):
    def __init__(self, parent, controller=None, **kwargs):
        super().__init__(parent, fg_color=Theme.QUARTERNARY, **kwargs)
        self.controller = controller

        self.create_title_section()

        # Container chính chứa hai cột
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)

        self.create_camera_section()
        self.create_control_section()
        self.create_back_button()

        # Biến camera
        self.cap = None

        self.model, self.label_encoder = load_model_and_encoder(
            "d:/DHBK/3.2/Pbl-5/WebApp/models/best_model.resolved.h5",
            "d:/DHBK/3.2/Pbl-5/WebApp/models/label_encoder.resolved.pkl"
        )

        # Initialize Mediapipe
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

    def create_title_section(self):
        """Tạo phần tiêu đề riêng biệt trên cùng"""
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(72, 12))

        self.title_label = ctk.CTkLabel(
            title_frame, text="Start your posture monitoring session",
            font=(Theme.FONT_FAMILY, Theme.FONT_3XL, "bold"), text_color=Theme.BLACK
        )
        self.title_label.pack()

        self.desc_label = ctk.CTkLabel(
            title_frame, text="Adjust your position and posture for better sitting",
            font=(Theme.FONT_FAMILY, Theme.FONT_XL), text_color=Theme.BLACK
        )
        self.desc_label.pack(pady=(12, 0))

    def create_camera_section(self):
        """Khung camera (bên trái)"""
        self.camera_frame = ctk.CTkFrame(
            self.container, fg_color=Theme.WHITE, width=448, height=293
        )
        self.camera_frame.grid(row=0, column=0, padx=(0, 10), pady=20, sticky="ne")

        self.camera_label = ctk.CTkLabel(self.camera_frame, text="No Camera Feed", width=448, height=293)
        self.camera_label.pack()

    def create_control_section(self):
        """Tạo phần điều khiển (bên phải)"""
        control_frame = ctk.CTkFrame(self.container, fg_color="transparent", width=468, height=278)
        control_frame.grid(row=0, column=1, padx=(10, 0), pady=20, sticky="nw")

        address_label = ctk.CTkLabel(
            control_frame, text="Choose your camera", anchor="w",
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE), text_color=Theme.BLACK
        )
        address_label.pack(fill="x")

        self.camera_selection = ctk.CTkComboBox(
            control_frame,
            values=["Laptop Camera (Default)"],  # Chỉ có 1 lựa chọn
            width=355, height=45,
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE),
            dropdown_font=(Theme.FONT_FAMILY, Theme.FONT_L),
            state="readonly", fg_color=Theme.WHITE, text_color=Theme.BLACK,
            dropdown_fg_color=Theme.WHITE, dropdown_text_color=Theme.BLACK,
            border_width=2, border_color=Theme.BLACK, corner_radius=Theme.ROUNDED_3
        )
        self.camera_selection.pack(pady=(0, 12), anchor="w")

        duration_label = ctk.CTkLabel(
            control_frame, text="Duration", anchor="w",
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE), text_color=Theme.BLACK
        )
        duration_label.pack(fill="x")

        self.time_selection = ctk.CTkComboBox(
            control_frame,
            values=["1 min", "2 min", "5 min", "10 min"],
            width=155, height=40,
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE),
            dropdown_font=(Theme.FONT_FAMILY, Theme.FONT_L),
            state="readonly", fg_color=Theme.WHITE, text_color=Theme.BLACK,
            dropdown_fg_color=Theme.WHITE, dropdown_text_color=Theme.BLACK,
            border_width=2, border_color=Theme.BLACK, corner_radius=Theme.ROUNDED_3
        )
        self.time_selection.pack(pady=(0, 20), anchor="w")

        self.start_button = ButtonFactory.create_dark_button(control_frame, "Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=(0, 20), anchor="w")

    def create_back_button(self):
        """Nút Go Back"""
        self.back_button = ctk.CTkButton(
            self.container,
            text="Go Back",
            fg_color="transparent",
            hover_color=Theme.LIGHT_PURPLE,
            text_color=Theme.PRIMARY_DARK,
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE, "underline"),
            width=0, height=0,
            command=self.go_back
        )
        self.back_button.grid(row=1, column=0, columnspan=2, pady=(20, 20))

    def update_video(self):
        """Cập nhật luồng video và vẽ đường keypoints"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Chuyển đổi màu OpenCV từ BGR -> RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_rgb.flags.writeable = False

                # Xử lý bằng MediaPipe
                results = pose.process(frame_rgb)
                frame_rgb.flags.writeable = True

                # Nếu phát hiện tư thế, vẽ lên ảnh
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                    )

                    # Dự đoán tư thế và hiển thị nhãn
                    keypoints = self.extract_keypoints(frame_rgb)
                    if keypoints is not None:
                        keypoints = np.expand_dims(keypoints, axis=0)
                        keypoints = keypoints.reshape((1, 33, 3, 1))
                        prediction = self.model.predict(keypoints, verbose=0)
                        posture_label = self.get_multiple_predictions(prediction, threshold=0.5)
                        self.display_postures(frame_rgb, posture_label)

                # Chuyển đổi sang ảnh Tkinter
                frame_rgb = cv2.resize(frame_rgb, (448, 293))  
                img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
                self.camera_label.configure(image=img, text="")  
                self.camera_label.image = img

        self.after(30, self.update_video)

    def start_monitoring(self):
        """Bắt đầu nhận diện camera"""
        print("Starting camera...")
        
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)  # Mở camera mặc định
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 448)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 293)
            if not self.cap.isOpened():
                print("Camera không thể mở!")
                return
        self.update_video()  # Cập nhật hình ảnh

    def stop_camera(self):
        """Dừng camera"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
            self.camera_label.configure(text="No Camera Feed", image="")  # Hiển thị lại chữ mặc định

    def go_back(self):
        """Quay lại màn hình trước"""
        self.stop_camera()  # Dừng camera khi thoát
        if self.controller:
            self.controller.show_frame("monitor")
    
    def extract_keypoints(self, image):
        results = self.pose.process(image)
        if results.pose_landmarks:
            keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
            return keypoints
        else:
            return None

    def extract_head_keypoints(self, image):
        """Extract head keypoints (nose, eyes, ears)"""
        results = self.pose.process(image)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            head_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # MediaPipe indices for head landmarks
            head_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in head_indices]).flatten()
            return head_points
        return None

    def extract_body_keypoints(self, image):
        """Extract torso keypoints (shoulders, chest, hips)"""
        results = self.pose.process(image)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            body_indices = [11, 12, 23, 24]  # MediaPipe indices for body landmarks
            body_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in body_indices]).flatten()
            return body_points
        return None

    def extract_arm_keypoints(self, image):
        """Extract arm keypoints (shoulders to wrists)"""
        results = self.pose.process(image)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            arm_indices = [11, 13, 15, 12, 14, 16]  # MediaPipe indices for arm landmarks
            arm_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in arm_indices]).flatten()
            return arm_points
        return None

    def extract_leg_keypoints(self, image):
        """Extract leg keypoints (hips to ankles)"""
        results = self.pose.process(image)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            leg_indices = [23, 25, 27, 24, 26, 28]  # MediaPipe indices for leg landmarks
            leg_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in leg_indices]).flatten()
            return leg_points
        return None

    def extract_foot_keypoints(self, image):
        """Extract foot keypoints (feet landmarks)"""
        results = self.pose.process(image)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            foot_indices = [29, 30, 31, 32]  # MediaPipe indices for foot landmarks
            foot_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in foot_indices]).flatten()
            return foot_points
        return None

    def get_pose_results(self, image):
        """
        Get raw MediaPipe pose results for visualization.
        """
        results = self.pose.process(image)
        return results

    def get_multiple_predictions(self, prediction, threshold=0.5):
        # Implement logic to get multiple predictions above threshold
        # Example: return ["Good Posture"] if prediction[0][0] > threshold else ["Bad Posture"]
        predicted_label = self.label_encoder.inverse_transform([np.argmax(prediction)])
        return predicted_label

    def display_postures(self, frame, postures):
        # Implement logic to display postures on frame
        # Example: cv2.putText(frame, postures[0], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, postures[0], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)