from motion_detection import MotionDetector
from send_email import send_email

# Initialize motion detector
detector = MotionDetector(video_path=0)
detector.detect_motion()  # ✅ Correct method

# Send the last captured image
latest_image = "Captured/latest_detected.jpg"  # Modify this to dynamica`   0lly get the latest image
full_frame_path = "Captured/full_frame.jpg"    # You need to define this path

# Call send_email with both required arguments
send_email(latest_image, full_frame_path)
