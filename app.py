import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
from dotenv import load_dotenv

load_dotenv()  # load variables from .env
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Create database
def init_db():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

def send_email(name, email, message):

    sender = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    print("Sender:", sender)

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = sender
    msg["Subject"] = "New Portfolio Contact"

    body = f"""
Name: {name}
Email: {email}
Message: {message}
"""

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, sender, msg.as_string())
    server.quit()

    print("Email sent")
    # HTML Email content
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#0f172a; color:#ffffff; padding:20px;">
        <h2 style="color:#38bdf8;">New Message from Portfolio Contact Form</h2>
        <table style="width:100%; border-collapse: collapse;">
          <tr>
            <td style="padding:10px; border:1px solid #38bdf8;"><strong>Name:</strong></td>
            <td style="padding:10px; border:1px solid #38bdf8;">{name}</td>
          </tr>
          <tr>
            <td style="padding:10px; border:1px solid #38bdf8;"><strong>Email:</strong></td>
            <td style="padding:10px; border:1px solid #38bdf8;">{email}</td>
          </tr>
          <tr>
            <td style="padding:10px; border:1px solid #38bdf8;"><strong>Message:</strong></td>
            <td style="padding:10px; border:1px solid #38bdf8;">{message}</td>
          </tr>
        </table>
        <p style="margin-top:20px; color:#94a3b8;">This message was sent from your portfolio contact form.</p>
      </body>
    </html>
    """

    # Attach HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Send email via Gmail SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.json

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        send_email(name, email, message)

        return jsonify({"message": "Message sent successfully"}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"message": "Server error"}), 500
    
    # Save to DB
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages(name,email,message) VALUES (?,?,?)",
        (name,email,message)
    )
    conn.commit()
    conn.close()

    # Try sending email
    try:
        send_email(name, email, message)
        email_status = "Email sent"
    except Exception as e:
        print("Email error:", e)
        email_status = "Email failed"

    return jsonify({"message": f"Message stored. {email_status}"})


@app.route("/messages")
def messages():

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()

    conn.close()

    messages = []

    for r in rows:
        messages.append({
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "message": r[3]
        })

    return jsonify(messages)

@app.route("/admin-login", methods=["POST"])
def admin_login():

    data = request.json

    username = data["username"]
    password = data["password"]

    if username == "admin" and password == "1234":
        return jsonify({"status":"success"})
    
    return jsonify({"status":"failed"})
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_message(id):

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages WHERE id=?", (id,))
    
    conn.commit()
    conn.close()

    return jsonify({"message":"Deleted"})
# IMPORTANT: run the server
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
