import cv2
import numpy as np
import pygame
import os
import time
from datetime import datetime
from ultralytics import YOLO
from threading import Thread
from send_email import send_email

class MotionDetector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"XVID"))

        self.model = YOLO("yolov8s.pt")

        self.target_classes = ['person']

        pygame.init()
        self.alarm_path = "Alarm/alarm.wav"
        try:
            pygame.mixer.music.load(self.alarm_path)
        except pygame.error:
            print(f"Alarm file not found: {self.alarm_path}")

        self.pts = []
        self.save_folder = None
        self.count = 0
        self.number_of_photos = 3
        self.frame_skip = 2
        self.frame_count = 0

        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Video", self.draw_polygon)

    def draw_polygon(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"Point Added: ({x}, {y})")
            self.pts.append([x, y])
        elif event == cv2.EVENT_RBUTTONDOWN:
            print("ROI Reset!")
            self.pts = []

    def inside_polygon(self, point):
        if len(self.pts) < 3:
            return False
        pts_array = np.array(self.pts, np.int32)
        return cv2.pointPolygonTest(pts_array, (point[0], point[1]), False) >= 0

    def save_detected_images(self, frame, person_img):
        if self.save_folder is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M%p")
            self.save_folder = f"Captured/{timestamp}"
            os.makedirs(f"{self.save_folder}/Full Frame", exist_ok=True)
            os.makedirs(f"{self.save_folder}/Person", exist_ok=True)

        frame_name = f"{self.save_folder}/Full Frame/frame_{int(time.time())}.jpg"
        person_name = f"{self.save_folder}/Person/person_{int(time.time())}.jpg"

        cv2.imwrite(frame_name, frame)
        cv2.imwrite(person_name, person_img)

        Thread(target=send_email, args=(person_name, frame_name)).start()

    def detect_motion(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.frame_count += 1
            if self.frame_count % self.frame_skip != 0:
                continue

            frame_detected = frame.copy()
            results = self.model.predict(frame, conf=0.4)

            person_detected = False

            overlay = frame.copy()
            if len(self.pts) >= 3:
                cv2.fillPoly(overlay, [np.array(self.pts, np.int32)], (0, 255, 0))
                frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    score = float(box.conf[0])
                    class_id = int(box.cls[0])
                    if class_id == 0:
                        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
                        cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                        if len(self.pts) >= 3 and self.inside_polygon((center_x, center_y)):
                            person_detected = True
                            person_img = frame_detected[y1:y2, x1:x2]

                            if self.count < self.number_of_photos:
                                self.save_detected_images(frame_detected, person_img)
                                self.count += 1

                            if not pygame.mixer.music.get_busy():
                                try:
                                    pygame.mixer.music.play()
                                except pygame.error:
                                    pass

                            cv2.putText(frame, "Person Detected!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows() ;