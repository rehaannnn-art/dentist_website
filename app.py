from flask import Flask, render_template, request, Response
import csv
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# ==========================
# Gmail Configuration
# ==========================
EMAIL_ADDRESS = "goldenrehan465@gmail.com"
EMAIL_PASSWORD = "YOUR_NEW_APP_PASSWORD"

CSV_FILE = "appointments.csv"


# ==========================
# Home Page
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Appointment Form
# ==========================
@app.route("/appointment", methods=["POST"])
def appointment():

    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    date = request.form["date"]
    treatment = request.form["treatment"]
    message = request.form["message"]

    print("\n========== NEW APPOINTMENT ==========")
    print("Name:", name)
    print("Phone:", phone)
    print("Email:", email)
    print("Date:", date)
    print("Treatment:", treatment)
    print("Message:", message)
    print("=====================================\n")

    # Create CSV file if it doesn't exist
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Name",
                "Phone",
                "Email",
                "Date",
                "Treatment",
                "Message"
            ])

        writer.writerow([
            name,
            phone,
            email,
            date,
            treatment,
            message
        ])

    # Send Email (works after adding your App Password)
    if EMAIL_PASSWORD != "YOUR_NEW_APP_PASSWORD":

        subject = "New Appointment - Smile Dental Clinic"

        body = f"""
New Appointment Received

Name: {name}
Phone: {phone}
Email: {email}
Date: {date}
Treatment: {treatment}
Message: {message}
"""

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            print("✅ Email Sent Successfully!")

        except Exception as e:
            print("❌ Email Error:", e)

    return """
<!DOCTYPE html>
<html>
<head>

<title>Appointment Received</title>

<meta http-equiv="refresh" content="3;url=/">

<style>

body{
font-family:Arial;
background:#f5f5f5;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
margin:0;
}

.box{
background:white;
padding:40px;
border-radius:15px;
box-shadow:0 0 15px rgba(0,0,0,.2);
text-align:center;
}

h1{
color:green;
}

</style>

</head>

<body>

<div class="box">

<h1>✅ Appointment Booked Successfully!</h1>

<p>Thank you for contacting Smile Dental Clinic.</p>

<p>We will contact you shortly.</p>

<p>Redirecting to Homepage...</p>

</div>

</body>

</html>
"""


# ==========================
# Admin Dashboard
# ==========================
@app.route("/admin")
def admin():

    appointments = []

    if os.path.isfile(CSV_FILE):

        with open(CSV_FILE, newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:
                appointments.append(row)

    return render_template("admin.html", appointments=appointments)


# ==========================
# Run Flask
# ==========================
if __name__ == "__main__":
    app.run(debug=True)