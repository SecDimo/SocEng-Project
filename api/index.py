from flask import Flask, render_template_string, request, send_file, jsonify
from datetime import datetime
import csv
import os
import json

app = Flask(__name__)

# Vercel's /tmp is the only writable directory
LOG_FILE = "/tmp/click_log.csv"
TARGETS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "targets.json")


def load_targets():
    if os.path.exists(TARGETS_FILE):
        with open(TARGETS_FILE, "r") as f:
            return json.load(f)
    return {}


def log_click(tracking_id, ip_address, user_agent):
    targets = load_targets()
    target_info = targets.get(tracking_id, {})

    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp", "tracking_id", "name", "email",
                "ip_address", "user_agent"
            ])
        writer.writerow([
            datetime.now().isoformat(),
            tracking_id,
            target_info.get("name", "Unknown"),
            target_info.get("email", "Unknown"),
            ip_address,
            user_agent
        ])


LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Security Notice</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
      background: #f0f4f8;
      padding: 20px;
    }
    .container {
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.1);
      max-width: 560px;
      width: 100%;
      text-align: center;
      overflow: hidden;
    }
    .banner { background: #dc2626; color: white; padding: 24px; font-size: 48px; }
    .content { padding: 32px 28px; }
    h1 { color: #dc2626; font-size: 24px; margin-bottom: 16px; }
    p { color: #374151; font-size: 16px; line-height: 1.6; margin-bottom: 12px; }
    .tips {
      text-align: left; background: #fef2f2;
      border-radius: 8px; padding: 20px 24px; margin-top: 20px;
    }
    .tips h2 { font-size: 16px; color: #991b1b; margin-bottom: 10px; }
    .tips ul { padding-left: 20px; color: #374151; font-size: 14px; line-height: 1.8; }
    .footer { margin-top: 24px; font-size: 13px; color: #9ca3af; }
  </style>
</head>
<body>
  <div class="container">
    <div class="banner">&#9888;&#65039;</div>
    <div class="content">
      <h1>You Failed the Phishing Test!</h1>
      <p>This was a <strong>simulated phishing attempt</strong> conducted as part of
         an authorized security awareness exercise.</p>
      <p>Don't worry — no data was collected and no harm was done. But in a real
         attack, clicking that link could have compromised your account.</p>
      <div class="tips">
        <h2>How to spot phishing emails:</h2>
        <ul>
          <li>Check the sender's email address carefully</li>
          <li>Hover over links before clicking them</li>
          <li>Be suspicious of urgent or threatening language</li>
          <li>When in doubt, contact IT directly</li>
        </ul>
      </div>
      <p class="footer">This test was performed as part of a Macomb College security assessment.</p>
    </div>
  </div>
</body>
</html>
"""


@app.route("/t/<tracking_id>")
def track_click(tracking_id):
    log_click(
        tracking_id,
        request.headers.get("X-Forwarded-For", request.remote_addr),
        request.headers.get("User-Agent", "Unknown")
    )
    return render_template_string(LANDING_PAGE)


@app.route("/dashboard")
def dashboard():
    clicks = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            reader = csv.DictReader(f)
            clicks = list(reader)

    unique_ids = set(c["tracking_id"] for c in clicks)
    targets = load_targets()
    total_targets = len(targets)

    return render_template_string("""
    <!DOCTYPE html>
    <html><head><title>Phishing Dashboard</title>
    <style>
      body { font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }
      h1 { margin-bottom: 8px; }
      .stats { display: flex; gap: 20px; margin: 20px 0; }
      .stat { background: #f3f4f6; border-radius: 8px; padding: 20px; flex: 1; text-align: center; }
      .stat .num { font-size: 36px; font-weight: bold; color: #dc2626; }
      .stat .label { font-size: 14px; color: #6b7280; margin-top: 4px; }
      table { width: 100%; border-collapse: collapse; margin-top: 20px; }
      th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid #e5e7eb; font-size: 14px; }
      th { background: #f9fafb; font-weight: 600; }
      .note { margin-top: 16px; padding: 12px; background: #fef3c7; border-radius: 6px; font-size: 13px; color: #92400e; }
    </style></head><body>
      <h1>Phishing Campaign Dashboard</h1>
      <p style="color:#6b7280;">Results for your Vulnerability Analysis Report</p>
      <div class="stats">
        <div class="stat"><div class="num">{{ total_targets }}</div><div class="label">Emails Sent</div></div>
        <div class="stat"><div class="num">{{ unique }}</div><div class="label">Unique Clicks</div></div>
        <div class="stat"><div class="num">{{ total }}</div><div class="label">Total Clicks</div></div>
        <div class="stat"><div class="num">{{ rate }}%</div><div class="label">Click Rate</div></div>
      </div>
      <div class="note">Note: Vercel uses serverless functions, so logs reset when the function cold starts.
      Check the dashboard shortly after sending your campaign for best results.</div>
      <h2 style="margin-top:24px;">Click Log</h2>
      <table>
        <tr><th>Time</th><th>Name</th><th>Email</th><th>IP Address</th></tr>
        {% for c in clicks %}
        <tr>
          <td>{{ c.timestamp }}</td>
          <td>{{ c.name }}</td>
          <td>{{ c.email }}</td>
          <td>{{ c.ip_address }}</td>
        </tr>
        {% endfor %}
        {% if not clicks %}
        <tr><td colspan="4" style="text-align:center;color:#9ca3af;padding:40px;">No clicks yet. Waiting for targets to click...</td></tr>
        {% endif %}
      </table>
    </body></html>
    """,
        clicks=clicks,
        unique=len(unique_ids),
        total=len(clicks),
        total_targets=total_targets,
        rate=round((len(unique_ids) / total_targets * 100), 1) if total_targets > 0 else 0
    )


@app.route("/")
def home():
    return "Server is running. Go to /dashboard to view results."
