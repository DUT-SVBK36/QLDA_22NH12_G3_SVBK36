import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
import mediapipe as mp
import threading
import time

# Local imports
from components.button import ButtonFactory
from _config.theme import Theme
from utils.model_loader import load_model_and_encoder
from screens.monitor.detect.extract import extract_keypoints, get_multiple_predictions, display_postures
# Initialize MediaPipe
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
        self.current_image = None  # Store reference to current CTkImage
        self.camera_thread = None
        self.camera_active = False

        # Load model and encoder
        model_path = os.path.join(os.path.dirname(__file__), 'models/best_model.resolved.h5')
        encoder_path = os.path.join(os.path.dirname(__file__), 'models/label_encoder.resolved.pkl')
        self.model, self.label_encoder = load_model_and_encoder(model_path, encoder_path)

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
        
        # Create a label with no image initially
        self.camera_label = ctk.CTkLabel(
            self.camera_frame, 
            text="No Camera Feed",
            width=448, 
            height=293,
            fg_color=Theme.WHITE,
            text_color=Theme.BLACK,
            font=(Theme.FONT_FAMILY, Theme.FONT_XL)
        )
        self.camera_label.pack(expand=True, fill="both")

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

        self.start_button = ButtonFactory.create_dark_button(
            control_frame, 
            text="Start Monitoring", 
            command=self.toggle_camera
        )
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

    def toggle_camera(self):
        if self.camera_active:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self):
        """Bắt đầu nhận diện camera"""
        print("Starting camera...")
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)  # Mở camera mặc định
            if not self.cap.isOpened():
                print("Camera không thể mở!")
                return
            self.camera_active = True
            self.start_button.configure(
                text="Stop Monitoring",
                command=self.toggle_camera
            )
            self.camera_thread = threading.Thread(target=self.update_video)
            self.camera_thread.daemon = True
            self.camera_thread.start()

    def stop_camera(self):
        """Dừng camera"""
        self.camera_active = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        self.camera_label.configure(text="No Camera Feed", image="")
        self.start_button.configure(
            text="Start Monitoring",
            command=self.toggle_camera
        )

    def update_video(self):
        """Cập nhật luồng video và vẽ đường keypoints"""
        if not self.camera_active or self.cap is None or not self.cap.isOpened():
            return  # Không cập nhật nếu camera bị dừng

        ret, frame = self.cap.read()
        if ret:
            # Chuyển đổi màu OpenCV từ BGR -> RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb.flags.writeable = False

            results = pose.process(frame_rgb)
            frame_rgb.flags.writeable = True

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

                keypoints = extract_keypoints(results)
                if keypoints is not None:
                    keypoints = np.expand_dims(keypoints, axis=0)
                    keypoints = keypoints.reshape((1, 33, 3, 1))
                    prediction = self.model.predict(keypoints, verbose=0)
                    posture_label = get_multiple_predictions(self.label_encoder,prediction, threshold=0.5)
                    display_postures(frame_rgb, posture_label)

            frame_rgb = cv2.resize(frame_rgb, (448, 293))

            img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            self.camera_label.configure(image=img, text="")
            self.camera_label.image = img

        self.after(30, self.update_video)



    def go_back(self):
        """Quay lại màn hình trước"""
        self.stop_camera()  # Dừng camera khi thoát
        if self.controller:
            self.controller.show_frame("monitor")
    
    # def extract_keypoints(self, results):
    #     """Extract keypoints from MediaPipe results directly"""
    #     if results.pose_landmarks:
    #         keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
    #         return keypoints
    #     return None

    # def extract_head_keypoints(self, results):
    #     """Extract head keypoints (nose, eyes, ears)"""
    #     if results.pose_landmarks:
    #         landmarks = results.pose_landmarks.landmark
    #         head_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # MediaPipe indices for head landmarks
    #         head_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in head_indices]).flatten()
    #         return head_points
    #     return None

    # def extract_body_keypoints(self, results):
    #     """Extract torso keypoints (shoulders, chest, hips)"""
    #     if results.pose_landmarks:
    #         landmarks = results.pose_landmarks.landmark
    #         body_indices = [11, 12, 23, 24]  # MediaPipe indices for body landmarks
    #         body_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in body_indices]).flatten()
    #         return body_points
    #     return None

    # def extract_arm_keypoints(self, results):
    #     """Extract arm keypoints (shoulders to wrists)"""
    #     if results.pose_landmarks:
    #         landmarks = results.pose_landmarks.landmark
    #         arm_indices = [11, 13, 15, 12, 14, 16]  # MediaPipe indices for arm landmarks
    #         arm_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in arm_indices]).flatten()
    #         return arm_points
    #     return None

    # def extract_leg_keypoints(self, results):
    #     """Extract leg keypoints (hips to ankles)"""
    #     if results.pose_landmarks:
    #         landmarks = results.pose_landmarks.landmark
    #         leg_indices = [23, 25, 27, 24, 26, 28]  # MediaPipe indices for leg landmarks
    #         leg_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in leg_indices]).flatten()
    #         return leg_points
    #     return None

    # def extract_foot_keypoints(self, results):
    #     """Extract foot keypoints (feet landmarks)"""
    #     if results.pose_landmarks:
    #         landmarks = results.pose_landmarks.landmark
    #         foot_indices = [29, 30, 31, 32]  # MediaPipe indices for foot landmarks
    #         foot_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in foot_indices]).flatten()
    #         return foot_points
    #     return None

    # def get_multiple_predictions(self, prediction, threshold=0.5):
    #     """Get prediction labels above threshold"""
    #     predicted_label = self.label_encoder.inverse_transform([np.argmax(prediction)])
    #     return predicted_label

    # def display_postures(self, frame, postures):
    #     """Display posture labels on the frame"""
    #     # Convert posture name to string if it's not already
    #     posture_text = str(postures[0]) if isinstance(postures, (list, np.ndarray)) else str(postures)
        
    #     # Add text to frame with proper font scale and positioning
    #     cv2.putText(
    #         frame,
    #         posture_text,
    #         (20, 40),  # Position at top-left with some margin
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         1,  # Font scale
    #         (255, 0, 0),  # Blue color in RGB
    #         2,  # Line thickness
    #         cv2.LINE_AA  # Anti-aliased line type
    #     )