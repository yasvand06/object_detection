# Object Detection Security System

This project is a Python-based smart security monitoring system that uses a webcam feed and computer vision to detect motion and identify people in real time. When a person is detected, the program can save images, play an alarm sound, and send email alerts.

## Features

- Live video monitoring from a webcam
- Person detection using YOLOv8
- Region-of-interest selection with mouse clicks
- Saving full-frame and cropped-person images
- Audio alarm playback
- Email notification support

## Project Structure

- `main.py` - Entry point for running the system
- `motion_detection.py` - Handles video capture, object detection, ROI selection, and alerts
- `image_capture.py` - Utility for saving captured images
- `alarm.py` - Alarm trigger logic
- `send_email.py` - Sends alert emails with attachments
- `yolov8s.pt` - YOLOv8 small model weights
- `Alarm/` - Audio files used for alerts
- `Captured/` - Output images captured during detection

## Requirements

Install the dependencies below before running the project:

```bash
pip install opencv-python numpy pygame ultralytics
```

## Setup

1. Clone the repository.
2. Make sure the model file `yolov8s.pt` is present in the project folder.
3. Set your email environment variables if you want email alerts:

```bash
set EMAIL_SENDER=your_email@gmail.com
set EMAIL_PASSWORD=your_app_password
set EMAIL_RECEIVER=recipient_email@gmail.com
```

4. Run the application:

```bash
python main.py
```

## Usage Notes

- Press `q` to quit the video window.
- Click on the video window to define a region of interest (ROI).
- Right-click to reset the ROI.
- The script saves captured images under the `Captured/` folder.

## Notes

- This project is intended for educational and personal security monitoring use.
- The email feature requires a valid SMTP setup and an app password for Gmail.

## License

This project is for learning and personal use.

## Team Members & Contributions

- **Praveen M**
  - YOLOv8 integration
  - Object detection testing and debugging
  - Documentation and project integration

- **Yasvand A K**
  - Motion detection logic
  - Region of Interest (ROI) implementation
  - Image capture functionality

- **Vishnu Kumar S**
  - Email alert system
  - Alarm integration
  - Project testing and deployment
