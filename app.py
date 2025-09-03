from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change in production

# Email setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_ADDRESS")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")

mail = Mail(app)

# Database setup
def init_db():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            subscribed_on TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            flash("Please fill out all fields", "error")
            return redirect("/")

        try:
            conn = sqlite3.connect('subscribers.db')
            c = conn.cursor()
            c.execute("INSERT INTO subscribers (name, email, subscribed_on) VALUES (?, ?, ?)",
                      (name, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()

            flash("Successfully subscribed!", "success")
        except sqlite3.IntegrityError:
            flash("You are already subscribed!", "info")
        return redirect("/")

    return render_template("index.html")

# Function to send daily emails
def send_daily_emails():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute("SELECT name, email FROM subscribers")
    subscribers = c.fetchall()
    conn.close()

    for name, email in subscribers:
        msg = Message(
            subject=f"College Knowledge Drop - {datetime.now().strftime('%B %d, %Y')}",
            sender=os.getenv("EMAIL_ADDRESS"),
            recipients=[email]
        )
        # Render email HTML
        msg.html = render_template("email_template.html", name=name)
        try:
            mail.send(msg)
            print(f"Email sent to {email}")
        except Exception as e:
            print(f"Failed to send to {email}: {e}")

if __name__ == "__main__":
    app.run(debug=True)
