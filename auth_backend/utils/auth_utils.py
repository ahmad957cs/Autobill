# auth_backend/utils/auth_utils.py

from auth_backend.create_app import bcrypt
import os
from dotenv import load_dotenv
load_dotenv()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")

def check_password(password, hashed):
    return bcrypt.check_password_hash(hashed, password)

def send_verification_email(to_email, verification_code, email_type="register"):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os
    from dotenv import load_dotenv

    load_dotenv()
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    if email_type == "register":
        subject = "Welcome! Verify your email for SmartBillCalc"
        body = f"""
        <h2>Congratulations on Registering!</h2>
        <p>Thank you for signing up for <b>SmartBillCalc</b>.</p>
        <p>Your verification code is:</p>
        <h1 style='color:#2d8cf0;'>{verification_code}</h1>
        <p>Please enter this code in the app to verify your account.</p>
        <br>
        <p>If you did not register, please ignore this email.</p>
        """
    elif email_type == "forgot":
        subject = "Password Reset Request for SmartBillCalc"
        body = f"""
        <h2>Password Reset Requested</h2>
        <p>We received a request to reset your password for <b>SmartBillCalc</b>.</p>
        <p>Your password reset code is:</p>
        <h1 style='color:#e67e22;'>{verification_code}</h1>
        <p>Enter this code in the app to set a new password.</p>
        <br>
        <p>If you did not request a password reset, you can safely ignore this email.</p>
        """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
