"""
Phishing Email Sender
======================
Reads targets from a CSV file and sends phishing emails with unique tracking links.
Styled to match Macomb College Communications email format.

Usage:
    1. Fill in targets.csv with name,email columns
    2. Update the CONFIG section below
    3. Run: python3 sender.py
"""

import csv
import json
import smtplib
import uuid
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


# ============================================================
# CONFIG — UPDATE THESE BEFORE RUNNING
# ============================================================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_throwaway@gmail.com"          # Your throwaway Gmail
SENDER_PASSWORD = "your_16_char_app_password"       # Gmail App Password
SENDER_DISPLAY_NAME = "Communications"

# This is the "From" address recipients will see
DISPLAY_FROM_EMAIL = "communications@macornb.info"

# Professor's email — will be BCC'd on every email
PROFESSOR_EMAIL = "naboznyk@macomb.edu"

# Your tracking server URL (update after deploying to Render)
TRACKING_SERVER_URL = "https://your-app-name.onrender.com"

# Input/output files
TARGETS_CSV = "targets.csv"
TARGETS_JSON = "targets.json"
SEND_LOG = "send_log.csv"

# Sending settings
DELAY_BETWEEN_EMAILS = 2   # seconds between each email
BATCH_SIZE = 50             # pause after this many emails
BATCH_PAUSE = 60            # seconds to pause between batches


# ============================================================
# EMAIL TEMPLATE — MATCHES MACOMB COMMUNICATIONS STYLE
# ============================================================

SUBJECT = "Important: Verify Your Account Information"

def build_email_body(name, tracking_url):
    first_name = name.split()[0] if name else "Employee"

    return f"""<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Important: Verify Your Account Information</title>
</head>
<body style="height:100%;margin:0;padding:0;width:100%;background-color:#f3ecd1;">

<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#f3ecd1;">
<tr>
<td align="center" style="padding:10px;border-top:4px inset #003399;">

<table border="0" cellpadding="0" cellspacing="0" width="600" style="max-width:600px;border:1px none #c7bb8e;">

<tr>
<td style="background-color:#f3ecd1;padding:8px 18px;text-align:center;">
    <span style="color:#003399;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:12px;">
        View this email in your browser
    </span>
</td>
</tr>

<tr>
<td style="background-color:#003399;padding:20px 18px;text-align:center;">
    <span style="color:#ffffff;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:22px;font-weight:bold;">
        Macomb Community College
    </span>
    <br>
    <span style="color:#c7bb8e;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:13px;">
        Information Technology Services
    </span>
</td>
</tr>

<tr>
<td style="background-color:#ffffff;padding:0;">
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;background-color:#FFFFFF;">
<tr>
<td style="padding:18px;color:#000000;font-family:Helvetica,sans-serif;font-size:14px;font-weight:normal;line-height:150%;text-align:left;">

<div style="text-align:left;">
As part of our ongoing efforts to enhance campus security, the Information Technology
department is conducting a routine verification of all employee accounts.<br>
<br>
We need all Macomb employees to confirm their account information by
<strong>Friday of this week</strong>. This process should take less than two minutes
to complete and will help us ensure the security of your account.<br>
<br>
This verification is being conducted in coordination with the
<strong>Office of the Vice President of Information Technology</strong>.
Your prompt attention to this matter is appreciated.<br>
<br>
<em>Failure to verify your account may result in a temporary suspension of
access to college systems including email, Canvas, and Banner.</em><br>
<br>
</div>

<table border="0" cellpadding="0" cellspacing="0" width="100%">
<tr>
<td align="center" style="padding:10px 18px 28px 18px;">
    <table border="0" cellpadding="0" cellspacing="0">
    <tr>
    <td align="center" style="border-radius:4px;background-color:#003399;">
        <a href="{tracking_url}" target="_blank"
           style="display:inline-block;padding:14px 40px;font-family:Helvetica,sans-serif;
                  font-size:14px;font-weight:bold;color:#ffffff;text-decoration:none;
                  border-radius:4px;background-color:#003399;border:1px solid #003399;">
            Verify Your Account Now
        </a>
    </td>
    </tr>
    </table>
</td>
</tr>
</table>

<div style="text-align:left;font-family:Helvetica,sans-serif;font-size:14px;color:#000000;line-height:150%;">
If you have any questions about this process, please contact the
<a href="mailto:helpdesk@macomb.edu" style="color:#003399;font-weight:normal;text-decoration:underline;">
IT Help Desk</a>.
</div>

</td>
</tr>
</table>
</td>
</tr>

<tr>
<td style="background-color:#003399;padding:18px;text-align:center;">
    <span style="color:#ffffff;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:11px;line-height:125%;">
        This message has been sent to Macomb Community College employees from the
        college's Information Technology department.
        <br><br>
        Macomb Community College &middot; 14500 E 12 Mile Rd &middot; Warren, MI 48088-3870 &middot; USA
    </span>
</td>
</tr>

</table>
</td>
</tr>
</table>

</body>
</html>"""


# ============================================================
# SENDER LOGIC
# ============================================================

def load_targets(csv_path):
    targets = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            targets.append({
                "name": row.get("name", "").strip(),
                "email": row.get("email", "").strip()
            })
    return targets


def generate_tracking_id():
    return uuid.uuid4().hex[:10]


def send_email(smtp_conn, target, tracking_id):
    tracking_url = f"{TRACKING_SERVER_URL}/t/{tracking_id}"

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{SENDER_DISPLAY_NAME} <{DISPLAY_FROM_EMAIL}>"
    msg["To"] = target["email"]
    msg["Subject"] = SUBJECT

    body = build_email_body(target["name"], tracking_url)
    msg.attach(MIMEText(body, "html"))

    recipients = [target["email"], PROFESSOR_EMAIL]
    smtp_conn.sendmail(SENDER_EMAIL, recipients, msg.as_string())


def log_sent(tracking_id, target):
    file_exists = os.path.exists(SEND_LOG)
    with open(SEND_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "tracking_id", "name", "email", "status"])
        writer.writerow([
            datetime.now().isoformat(),
            tracking_id,
            target["name"],
            target["email"],
            "sent"
        ])


def save_targets_json(mapping):
    with open(TARGETS_JSON, "w") as f:
        json.dump(mapping, f, indent=2)


def main():
    targets = load_targets(TARGETS_CSV)
    print(f"Loaded {len(targets)} targets from {TARGETS_CSV}")

    if not targets:
        print("No targets found. Check your CSV file.")
        return

    target_mapping = {}
    send_queue = []
    for t in targets:
        tid = generate_tracking_id()
        target_mapping[tid] = {"name": t["name"], "email": t["email"]}
        send_queue.append((t, tid))

    save_targets_json(target_mapping)
    print(f"Saved tracking IDs to {TARGETS_JSON}")

    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("Connected!\n")

    sent = 0
    failed = 0
    for i, (target, tid) in enumerate(send_queue, 1):
        try:
            send_email(smtp, target, tid)
            log_sent(tid, target)
            sent += 1
            print(f"[{i}/{len(send_queue)}] Sent to {target['email']}")
        except Exception as e:
            failed += 1
            print(f"[{i}/{len(send_queue)}] FAILED: {target['email']} — {e}")

        time.sleep(DELAY_BETWEEN_EMAILS)

        if i % BATCH_SIZE == 0 and i < len(send_queue):
            print(f"\n--- Pausing {BATCH_PAUSE}s after batch of {BATCH_SIZE} ---\n")
            time.sleep(BATCH_PAUSE)

    smtp.quit()

    print(f"\n{'='*40}")
    print(f"COMPLETE: {sent} sent, {failed} failed")
    print(f"Send log: {SEND_LOG}")
    print(f"Target map: {TARGETS_JSON}")
    print(f"Copy {TARGETS_JSON} to your GitHub repo so Render picks it up.")
    print(f"{'='*40}")


if __name__ == "__main__":
    main()
