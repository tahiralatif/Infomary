import smtplib
import os
import uuid
import asyncio
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import gspread
import json
from google.oauth2.service_account import Credentials
import sendgrid

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────────────────────────
SMTP_HOST        = "smtp.gmail.com"
SMTP_PORT        = 587
SENDER_EMAIL     = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD  = os.getenv("SENDER_PASSWORD")
SHEET_URL        = "https://docs.google.com/spreadsheets/d/1sJYvoP4BOVeMWaFGBOPTtpuJKrY847n3GQzElQyPRKY/edit?usp=sharing"
CREDENTIALS_FILE = "credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# ═══════════════════════════════════════════════════════════════════════════════
# TOOL 1 — SAVE TO GOOGLE SHEET
# ═══════════════════════════════════════════════════════════════════════════════
async def tool_save_to_sheet(lead: dict) -> dict:
    """
    Tool 1: Saves user lead data to Google Sheet.
    """
    print("[Tool 1] Saving to Google Sheet...")
    try:
        loop = asyncio.get_event_loop()

        def _save():
            creds_json = os.getenv("GOOGLE_CREDENTIALS")
            if creds_json:
                creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
            else:
                creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
            client = gspread.authorize(creds)
            sheet  = client.open_by_url(SHEET_URL).sheet1
            sheet.append_row([
                lead["lead_id"],
                lead["name"],
                lead["email"],
                lead["phone"],
                lead["care_need"],
                lead["location"],
                lead["status"],
                lead["notes"],
                lead["saved_at"],
            ])

        await loop.run_in_executor(None, _save)
        print("[Tool 1] ✓ Lead saved to Google Sheet")
        return {"success": True, "message": "Lead saved to Google Sheet"}

    except Exception as e:
        print(f"[Tool 1] ✗ Sheet error → {e}")
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════════════════════════
# TOOL 2 — SEND CONFIRMATION EMAIL
# ═══════════════════════════════════════════════════════════════════════════════
def build_html_email(lead: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:'Segoe UI',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 0;">
  <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0"
           style="background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

      <!-- HEADER -->
      <tr>
        <td style="background:linear-gradient(135deg,#1a73e8,#0d47a1);padding:40px 48px;text-align:center;">
          <h1 style="margin:0;color:#fff;font-size:26px;font-weight:700;">
            InfoSenior<span style="color:#90caf9;">.care</span>
          </h1>
          <p style="margin:8px 0 0;color:#bbdefb;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;">
            New Lead Notification
          </p>
        </td>
      </tr>

      <!-- ALERT BADGE -->
      <tr>
        <td style="background:#e8f0fe;padding:18px 48px;border-bottom:1px solid #c5d4f5;">
          <p style="margin:0;color:#1a47a1;font-size:14px;font-weight:600;">
            A new lead has been captured via Infomary — please follow up promptly.
          </p>
        </td>
      </tr>

      <!-- BODY -->
      <tr>
        <td style="padding:44px 48px;">

          <p style="margin:0 0 28px;color:#1a1a2e;font-size:20px;font-weight:700;">
            New Lead Details
          </p>

          <!-- Details Table -->
          <table width="100%" cellpadding="0" cellspacing="0"
                 style="border:1px solid #e0e0e0;border-radius:8px;overflow:hidden;margin-bottom:32px;">
            <tr style="background:#f8f9ff;">
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;width:40%;">
                <p style="margin:0;color:#888;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Full Name</p>
              </td>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#1a1a2e;font-size:14px;font-weight:600;">{lead['name']}</p>
              </td>
            </tr>
            <tr>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;background:#f8f9ff;">
                <p style="margin:0;color:#888;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Email Address</p>
              </td>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#1a73e8;font-size:14px;">{lead['email']}</p>
              </td>
            </tr>
            <tr style="background:#f8f9ff;">
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#888;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Phone Number</p>
              </td>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#1a1a2e;font-size:14px;">{lead['phone']}</p>
              </td>
            </tr>
            <tr>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;background:#f8f9ff;">
                <p style="margin:0;color:#888;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Care Need</p>
              </td>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#1a1a2e;font-size:14px;">{lead['care_need']}</p>
              </td>
            </tr>
            <tr style="background:#f8f9ff;">
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#888;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Location</p>
              </td>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#1a1a2e;font-size:14px;">{lead['location']}</p>
              </td>
            </tr>
            <tr>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;background:#f8f9ff;">
                <p style="margin:0;color:#888;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Notes</p>
              </td>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#1a1a2e;font-size:14px;">{lead['notes'] or 'N/A'}</p>
              </td>
            </tr>
            <tr style="background:#f8f9ff;">
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#888;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Lead ID</p>
              </td>
              <td style="padding:12px 20px;border-bottom:1px solid #e0e0e0;">
                <p style="margin:0;color:#1a1a2e;font-size:14px;font-weight:700;letter-spacing:1px;">{lead['lead_id']}</p>
              </td>
            </tr>
            <tr>
              <td style="padding:12px 20px;background:#f8f9ff;">
                <p style="margin:0;color:#888;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Captured At</p>
              </td>
              <td style="padding:12px 20px;">
                <p style="margin:0;color:#1a1a2e;font-size:14px;">{lead['saved_at']}</p>
              </td>
            </tr>
          </table>

          <p style="margin:0;color:#555;font-size:14px;line-height:1.8;">
            This lead was captured automatically via the Infomary AI voice assistant. 
            Please review the details above and initiate follow-up at your earliest convenience.
          </p>

        </td>
      </tr>

      <!-- FOOTER -->
      <tr>
        <td style="border-top:1px solid #ebebeb;padding:28px 48px;text-align:center;">
          <p style="margin:0 0 4px;color:#1a73e8;font-size:14px;font-weight:700;">InfoSenior.care</p>
          <p style="margin:0;color:#999;font-size:12px;">This is an automated internal notification. Please do not reply to this email.</p>
        </td>
      </tr>

    </table>
  </td></tr>
</table>
</body>
</html>"""

async def tool_send_email(lead: dict) -> dict:
    print("[Tool 2] Sending confirmation email...")
    try:
        import resend
        resend.api_key = os.getenv("RESEND_API_KEY")
        
        resend.Emails.send({
            "from": "InfoSenior.care <onboarding@resend.dev>",
            "to": SENDER_EMAIL,
            "subject": f"New Lead: {lead['name']} — {lead['care_need']} — {lead['location']}",
            "html": build_html_email(lead)
        })
        
        print(f"[Tool 2] ✓ Email sent")
        return {"success": True, "message": "Email sent successfully"}

    except Exception as e:
        print(f"[Tool 2] ✗ Email error → {e}")
        return {"success": False, "error": str(e)}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — RUN BOTH TOOLS IN PARALLEL
# ═══════════════════════════════════════════════════════════════════════════════
async def save_lead_and_notify(
    name: str,
    email: str,
    phone: str,
    care_need: str,
    location: str,
    notes: str = ""
) -> dict:
    """
    Runs Tool 1 (save to sheet) and Tool 2 (send email) in parallel.

    Args:
        name      : Full name of the user
        email     : Email address of the user
        phone     : Phone number of the user
        care_need : Type of care needed
        location  : City or ZIP code
        notes     : Extra notes (optional)

    Returns:
        dict: success, lead_id, sheet_result, email_result
    """

    lead = {
        "lead_id"  : str(uuid.uuid4())[:8].upper(),
        "name"     : name,
        "email"    : email,
        "phone"    : phone,
        "care_need": care_need,
        "location" : location,
        "status"   : "New",
        "notes"    : notes,
        "saved_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    print(f"\n{'='*50}")
    print(f"  New Lead → {name} | {care_need} | {location}")
    print(f"{'='*50}\n")

    # Run both tools in parallel
    sheet_result, email_result = await asyncio.gather(
        tool_save_to_sheet(lead),
        tool_send_email(lead),
    )

    print(f"\n{'='*50}")
    print(f"  Lead ID     : {lead['lead_id']}")
    print(f"  Sheet Saved : {'✓' if sheet_result['success'] else '✗'}")
    print(f"  Email Sent  : {'✓' if email_result['success'] else '✗'}")
    print(f"{'='*50}\n")

    return {
        "success"     : sheet_result["success"] and email_result["success"],
        "lead_id"     : lead["lead_id"],
        "sheet_result": sheet_result,
        "email_result": email_result,
    }




# ─── TEST ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(save_lead_and_notify(
        name      = "Ahmed Khan",
        email     = "tara378581@gmail.com",  # put your email here for testing
        phone     = "+92-300-1234567",
        care_need = "Memory Care",
        location  = "Houston, Texas",
        notes     = "Mother showing early signs of dementia"
    ))