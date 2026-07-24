"""
emailer.py
Sends the leads CSV report to your email via Gmail.

Requires a Gmail "App Password" (not your regular password) stored in .env:
  GMAIL_ADDRESS=youraddress@gmail.com
  GMAIL_APP_PASSWORD=GMAIL_APP_PASSWORD=xuyqappzciserngi
  REPORT_TO_EMAIL=whereyouwantitsent@gmail.com
"""

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
REPORT_TO_EMAIL = os.getenv("REPORT_TO_EMAIL", "")


def send_report_email(csv_filepath, lead_count):
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD or not REPORT_TO_EMAIL:
        print("Email not sent: missing GMAIL_ADDRESS, GMAIL_APP_PASSWORD, or REPORT_TO_EMAIL in .env")
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Lead Report - {lead_count} leads found"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = REPORT_TO_EMAIL
    msg.set_content(
        f"Your business lead agent just finished a run.\n\n"
        f"Total leads: {lead_count}\n"
        f"See the attached CSV for full details."
    )

    with open(csv_filepath, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(csv_filepath)
    msg.add_attachment(file_data, maintype="text", subtype="csv", filename=file_name)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        print(f"Emailed report to {REPORT_TO_EMAIL}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False