import os
import smtplib
from email.message import EmailMessage

# ✅ Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "recipient@example.com")


def send_email(person_image_path, full_frame_path):
    """Sends an email with the detected person image and full frame attached."""
    msg = EmailMessage()
    msg["Subject"] = "Security Alert: Person Detected!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("Alert! A person was detected in the restricted area. See the attached images.")

    # ✅ Attach Person Image
    with open(person_image_path, "rb") as img_file:
        img_data = img_file.read()
        msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename=os.path.basename(person_image_path))

    # ✅ Attach Full Frame Image
    with open(full_frame_path, "rb") as img_file:
        img_data = img_file.read()
        msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename=os.path.basename(full_frame_path))

    # ✅ Send Email
    if not EMAIL_PASSWORD:
        print("❌ Email password not configured. Set EMAIL_PASSWORD in your environment.")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent successfully with images: {person_image_path}, {full_frame_path}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
