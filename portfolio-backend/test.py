import smtplib
from email.mime.text import MIMEText

sender = "mastershiv8551@gmail.com"
password = "iqax httt efls oygg"
recipient = "mastershiv8551@gmail.com"

msg = MIMEText("Test email from Flask")
msg["Subject"] = "Test"
msg["From"] = sender
msg["To"] = recipient

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("Error:", e)