import os
import json
import urllib.request
import urllib.parse
from flask import Flask, render_template_string, request
from datetime import datetime
 
app = Flask(__name__)
 
# ============================================================
# SUPABASE CONFIG — UPDATE THESE
# ============================================================
SUPABASE_URL = "https://gohgblgjvdsnmuhiqejm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdvaGdibGdqdmRzbm11aGlxZWptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5ODQ5ODgsImV4cCI6MjA5MjU2MDk4OH0.wgfe-5HLsB5OtX-FaetWlv-55HfLY6rtb5ZjIg9MNRE" 
 
TARGETS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "targets.json")
 
 
def load_targets():
    if os.path.exists(TARGETS_FILE):
        with open(TARGETS_FILE, "r") as f:
            return json.load(f)
    return {}
 
 
def save_click_to_supabase(tracking_id, ip_address, user_agent):
    """Save click to Supabase database — permanent storage."""
    targets = load_targets()
    target_info = targets.get(tracking_id, {})
 
    data = json.dumps({
        "timestamp": datetime.now().isoformat(),
        "tracking_id": tracking_id,
        "name": target_info.get("name", "Unknown"),
        "email": target_info.get("email", "Unknown"),
        "ip_address": ip_address,
        "user_agent": user_agent
    }).encode("utf-8")
 
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/clicks",
        data=data,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        },
        method="POST"
    )
 
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Supabase error: {e}")
 
 
def get_clicks_from_supabase():
    """Retrieve all clicks from Supabase."""
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/clicks?select=*&order=timestamp.desc",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
    )
 
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Supabase read error: {e}")
        return []
 
 
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
 
 
@app.route("/t/test123")
def track_click(tracking_id):
    save_click_to_supabase(
        tracking_id,
        request.headers.get("X-Forwarded-For", request.remote_addr),
        request.headers.get("User-Agent", "Unknown")
    )
    return render_template_string(LANDING_PAGE)
 
 
@app.route("/dashboard")
def dashboard():
    clicks = get_clicks_from_supabase()
    unique_ids = set(c.get("tracking_id", "") for c in clicks)
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
      .badge { display: inline-block; background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 10px; font-size: 11px; }
    </style></head><body>
      <h1>Phishing Campaign Dashboard</h1>
      <p style="color:#6b7280;">Results for your Vulnerability Analysis Report
        <span class="badge">Logs saved permanently</span>
      </p>
      <div class="stats">
        <div class="stat"><div class="num">{{ total_targets }}</div><div class="label">Emails Sent</div></div>
        <div class="stat"><div class="num">{{ unique }}</div><div class="label">Unique Clicks</div></div>
        <div class="stat"><div class="num">{{ total }}</div><div class="label">Total Clicks</div></div>
        <div class="stat"><div class="num">{{ rate }}%</div><div class="label">Click Rate</div></div>
      </div>
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
 
