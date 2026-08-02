import cv2
import os
from datetime import datetime

# Global variable to store the execution folder name (created once per run)
execution_folder = None

def create_execution_folder():
    """Creates a new folder with the current date and time, only once per execution."""
    global execution_folder
    if execution_folder is None:
        current_time = datetime.now().strftime("%Y-%m-%d_%I-%M %p")  # Format: YYYY-MM-DD_HH-MM AM/PM
        execution_folder = os.path.join("Captured", current_time)
        os.makedirs(os.path.join(execution_folder, "Full Frame"), exist_ok=True)
        os.makedirs(os.path.join(execution_folder, "Person"), exist_ok=True)
    return execution_folder

def capture_and_save(frame, bbox):
    """Saves both the full frame and the detected person image."""
    folder_path = create_execution_folder()

    # Save full frame
    full_frame_path = os.path.join(folder_path, "Full Frame", "full_frame.jpg")
    cv2.imwrite(full_frame_path, frame)

    # Save cropped person image
    x1, y1, x2, y2 = bbox
    person_img = frame[y1:y2, x1:x2]  # Crop the detected person
    person_image_path = os.path.join(folder_path, "Person", "detected_person.jpg")
    cv2.imwrite(person_image_path, person_img)

    return full_frame_path, person_image_path  # Return paths for email sending
