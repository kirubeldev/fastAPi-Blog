from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import os
load_dotenv()

Sender = os.getenv("MY_EMAIL_FROM")
app_pass = os.getenv("GOOGLE_APP_PASSWORD")


def send_email(receiver:str , subject :str, html_content:str):

    msg =EmailMessage()

    msg["From"] = Sender
    msg["To"]= receiver
    msg["Subject"] = subject

    msg.add_alternative(html_content, subtype="html")
    with smtplib.SMTP_SSL("smtp.gmail.com" , 465) as smtp:
        smtp.login(Sender , app_pass)
        smtp.send_message(msg)






registration_html = """
<html>
  <body style="font-family: Arial, sans-serif; background-color:#f9f9f9; padding: 20px;">
    <div style="max-width: 600px; margin:auto; background-color:#fff; padding:20px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
      <h2 style="color:#0097FF;">Welcome to the Ultimate Blog Website!</h2>
      <p>Hi there,</p>
      <p>Thank you for signing up. We're excited to have you onboard!</p>
      <p>Start exploring and enjoy your experience.</p>
      <hr>
      <p style="font-size:12px; color:gray;">This is an automated message. Please do not reply.</p>
    </div>
  </body>
</html>
"""

login_html = """
<html>
  <body style="font-family: Arial, sans-serif; background-color:#f9f9f9; padding: 20px;">
    <div style="max-width: 600px; margin:auto; background-color:#fff; padding:20px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
      <h2 style="color:#0097FF;">New Login Alert</h2>
      <p>Hello,</p>
      <p>Your account was just used to login. If this was not you, please reset your password immediately!</p>
      <hr>
      <p style="font-size:12px; color:gray;">This is an automated message. Please do not reply.</p>
    </div>
  </body>
</html>
"""
