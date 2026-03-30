import json
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# ─── MOCK DATA (will be replaced by Google Sheets later) ──────────────────────
MOCK_USERS = [
    {"name": "Ahmed Khan",   "email": "ahmed@example.com",  "phone": "+92-300-1234567"},
    {"name": "Sara Ali",     "email": "sara@example.com",   "phone": "+92-311-9876543"},
    {"name": "Usman Raza",   "email": "usman@example.com",  "phone": "+92-321-5556789"},
    {"name": "Fatima Malik", "email": "fatima@example.com", "phone": "+92-333-4441122"},
    {"name": "Bilal Sheikh", "email": "bilal@example.com",  "phone": "+92-345-7778899"},
]

# ─── CONFIG ───────────────────────────────────────────────────────────────────
SMTP_HOST       = "smtp.gmail.com"
SMTP_PORT       = 587
SENDER_EMAIL    = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

JSON_FILE       = "saved_users.json"


# ─── HTML EMAIL TEMPLATE ──────────────────────────────────────────────────────
def build_html_email(name: str, email: str, phone: str, saved_at: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Data Confirmation</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f6f9;font-family:'Segoe UI',Arial,sans-serif;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#1a73e8,#0d47a1);padding:40px 48px;text-align:center;">
              <h1 style="margin:0;color:#ffffff;font-size:26px;font-weight:700;letter-spacing:-0.5px;">
                InfoSenior<span style="color:#90caf9;">.care</span>
              </h1>
              <p style="margin:8px 0 0;color:#bbdefb;font-size:13px;letter-spacing:1px;text-transform:uppercase;">
                AI-Powered Senior Care Platform
              </p>
            </td>
          </tr>

          <!-- Success Banner -->
          <tr>
            <td style="background:#e8f5e9;padding:20px 48px;text-align:center;border-bottom:1px solid #c8e6c9;">
              <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
                <tr>
                  <td style="background:#43a047;border-radius:50%;width:36px;height:36px;text-align:center;vertical-align:middle;">
                    <span style="color:#fff;font-size:20px;line-height:36px;">&#10003;</span>
                  </td>
                  <td style="padding-left:12px;">
                    <span style="color:#2e7d32;font-size:15px;font-weight:600;">
                      Your data has been successfully saved!
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:40px 48px;">

              <p style="margin:0 0 8px;color:#5f6368;font-size:13px;text-transform:uppercase;letter-spacing:1px;font-weight:600;">
                Hello,
              </p>
              <h2 style="margin:0 0 20px;color:#1a1a2e;font-size:22px;font-weight:700;">
                {name} 👋
              </h2>

              <p style="margin:0 0 28px;color:#444;font-size:15px;line-height:1.7;">
                We're glad to let you know that your information has been
                <strong>successfully recorded</strong> in the InfoSenior.care system.
                Below is a summary of the details we have on file for you.
              </p>

              <!-- Data Card -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#f8f9ff;border:1px solid #e3e8ff;border-radius:12px;overflow:hidden;margin-bottom:32px;">

                <tr style="background:#eef1ff;">
                  <td colspan="2" style="padding:14px 24px;">
                    <span style="color:#3949ab;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">
                      Your Saved Information
                    </span>
                  </td>
                </tr>

                <tr style="border-top:1px solid #e3e8ff;">
                  <td style="padding:14px 24px;color:#888;font-size:13px;font-weight:600;width:130px;">Full Name</td>
                  <td style="padding:14px 24px;color:#1a1a2e;font-size:14px;font-weight:600;">{name}</td>
                </tr>

                <tr style="background:#f0f3ff;border-top:1px solid #e3e8ff;">
                  <td style="padding:14px 24px;color:#888;font-size:13px;font-weight:600;">Email</td>
                  <td style="padding:14px 24px;color:#1a73e8;font-size:14px;">{email}</td>
                </tr>

                <tr style="border-top:1px solid #e3e8ff;">
                  <td style="padding:14px 24px;color:#888;font-size:13px;font-weight:600;">Phone</td>
                  <td style="padding:14px 24px;color:#1a1a2e;font-size:14px;">{phone}</td>
                </tr>

                <tr style="background:#f0f3ff;border-top:1px solid #e3e8ff;">
                  <td style="padding:14px 24px;color:#888;font-size:13px;font-weight:600;">Saved At</td>
                  <td style="padding:14px 24px;color:#1a1a2e;font-size:14px;">{saved_at}</td>
                </tr>

              </table>

              <p style="margin:0 0 28px;color:#444;font-size:15px;line-height:1.7;">
                If you notice any incorrect information or have any questions,
                please don't hesitate to reach out to our support team. We're
                always happy to help.
              </p>

              <!-- CTA Button -->
              <table cellpadding="0" cellspacing="0" style="margin-bottom:12px;">
                <tr>
                  <td style="background:linear-gradient(135deg,#1a73e8,#0d47a1);border-radius:8px;padding:14px 32px;text-align:center;">
                    <a href="https://infosenior.care" target="_blank"
                       style="color:#ffffff;font-size:14px;font-weight:700;text-decoration:none;letter-spacing:0.5px;">
                      Visit InfoSenior.care &rarr;
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:0 48px;">
              <hr style="border:none;border-top:1px solid #ebebeb;margin:0;" />
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:28px 48px;text-align:center;">
              <p style="margin:0 0 6px;color:#1a73e8;font-size:14px;font-weight:700;">
                InfoSenior.care Team
              </p>
              <p style="margin:0 0 4px;color:#999;font-size:12px;">
                AI-Powered Senior Care Platform &bull; United States
              </p>
              <p style="margin:0;color:#bbb;font-size:11px;">
                This is an automated message. Please do not reply directly to this email.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>
"""


# ─── SAVE TO JSON ─────────────────────────────────────────────────────────────
def save_to_json(users: list) -> str:
    existing = []
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            existing = json.load(f)

    for user in users:
        user["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_users = existing + users
    with open(JSON_FILE, "w") as f:
        json.dump(all_users, f, indent=4)

    print(f"[✓] {len(users)} users saved to JSON → {JSON_FILE}")
    return JSON_FILE


# ─── SEND ONE EMAIL ───────────────────────────────────────────────────────────
def send_confirmation_email(server, user: dict) -> bool:
    name     = user.get("name", "User")
    email    = user.get("email", "")
    phone    = user.get("phone", "-")
    saved_at = user.get("saved_at", "-")

    if not email:
        print(f"  [✗] {name} — email missing, skipping")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "✅ Your Data Has Been Successfully Saved — InfoSenior.care"
    msg["From"]    = f"InfoSenior.care <{SENDER_EMAIL}>"
    msg["To"]      = email

    # Plain text fallback
    plain = f"Dear {name}, your data has been saved. Name: {name} | Email: {email} | Phone: {phone} | Saved At: {saved_at}"
    msg.attach(MIMEText(plain, "plain"))

    # HTML version
    html = build_html_email(name, email, phone, saved_at)
    msg.attach(MIMEText(html, "html"))

    try:
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        print(f"  [✓] Email sent → {name} ({email})")
        return True
    except Exception as e:
        print(f"  [✗] Failed  → {name} ({email}) | {e}")
        return False


# ─── MAIN FUNCTION TOOL ───────────────────────────────────────────────────────
def process_and_notify_users(users: list = None) -> dict:
    """
    Saves user data to JSON and sends each user a beautiful
    HTML confirmation email.

    Args:
        users: List of dicts [{name, email, phone}]
               If None, MOCK_USERS will be used.

    Returns:
        dict: total, sent, failed, json_file
    """
    if users is None:
        users = MOCK_USERS
        print("[i] Using mock data\n")

    json_path = save_to_json(users)

    print(f"\n[i] Sending emails to {len(users)} users...\n")
    result = {"total": len(users), "sent": 0, "failed": 0, "json_file": json_path}

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
    except Exception as e:
        print(f"[✗] SMTP Error: {e}")
        result["error"] = str(e)
        return result

    for user in users:
        success = send_confirmation_email(server, user)
        if success:
            result["sent"] += 1
        else:
            result["failed"] += 1

    server.quit()

    print(f"\n{'='*45}")
    print(f"  Total   : {result['total']}")
    print(f"  Sent    : {result['sent']}")
    print(f"  Failed  : {result['failed']}")
    print(f"  JSON    : {result['json_file']}")
    print(f"{'='*45}")

    return result


# ─── AGENT TOOL (uncomment when adding to agent) ──────────────────────────────
# from agents import function_tool
# tool = function_tool(process_and_notify_users)


# ─── RUN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    process_and_notify_users()