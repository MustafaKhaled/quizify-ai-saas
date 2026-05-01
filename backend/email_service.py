import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

EMAIL_FROM = os.getenv("EMAIL_FROM", "Quizify <noreply@quizifyai.app>")
REPLY_TO = os.getenv("EMAIL_REPLY_TO", "hello@quizifyai.app")
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:3000")
# Marketing site — reset-password lives here since users are signed out when they click the email link.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")
COMPANY_ADDRESS = os.getenv("COMPANY_ADDRESS", "Quizify AI , Vienna, Austria")
UNSUBSCRIBE_URL = f"{FRONTEND_URL}/unsubscribe"


def _footer_html() -> str:
    return f"""
    <p style="color: #94a3b8; font-size: 10px; margin-top: 40px; text-align: center;">
        {COMPANY_ADDRESS} | <a href="{UNSUBSCRIBE_URL}" style="color: #94a3b8;">Unsubscribe</a>
    </p>
    """


def _list_unsubscribe_headers() -> dict:
    """Headers spam filters check to identify legitimate transactional/list mail."""
    return {
        "List-Unsubscribe": f"<{UNSUBSCRIBE_URL}>, <mailto:{REPLY_TO}?subject=unsubscribe>",
        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
    }


def send_verification_email(to_email: str, token: str):
    verification_url = f"{DASHBOARD_URL}/verify-email?token={token}"

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": [to_email],
        "reply_to": REPLY_TO,
        "subject": "Verify your email - Quizify",
        "headers": _list_unsubscribe_headers(),
        "text": (
            f"Welcome to Quizify!\n\n"
            f"Verify your email by visiting:\n{verification_url}\n\n"
            f"This link expires in 24 hours. If you didn't create an account, you can ignore this email.\n\n"
            f"{COMPANY_ADDRESS}\nUnsubscribe: {UNSUBSCRIBE_URL}"
        ),
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #1e293b;">Welcome to Quizify!</h2>
            <p style="color: #475569; font-size: 16px;">
                Thanks for signing up. Please verify your email address by clicking the button below:
            </p>
            <div style="text-align: center; margin: 32px 0;">
                <a href="{verification_url}"
                   style="background-color: #2563eb; color: white; padding: 12px 32px;
                          text-decoration: none; border-radius: 8px; font-weight: bold;
                          font-size: 16px; display: inline-block;">
                    Verify Email
                </a>
            </div>
            <p style="color: #64748b; font-size: 14px;">
                Or copy and paste this link into your browser:<br>
                <a href="{verification_url}" style="color: #2563eb;">{verification_url}</a>
            </p>
            <p style="color: #94a3b8; font-size: 12px; margin-top: 32px;">
                This link expires in 24 hours. If you didn't create an account, you can ignore this email.
            </p>
            {_footer_html()}
        </div>
        """
    })


def send_password_reset_email(to_email: str, token: str):
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": [to_email],
        "reply_to": REPLY_TO,
        "subject": "Reset your Quizify password",
        "headers": _list_unsubscribe_headers(),
        "text": (
            f"Reset your Quizify password\n\n"
            f"We received a request to reset the password for your account. "
            f"Open this link in your browser to choose a new one:\n{reset_url}\n\n"
            f"This link expires in 1 hour. If you didn't request a password reset, "
            f"you can safely ignore this email — your password won't change.\n\n"
            f"{COMPANY_ADDRESS}\nUnsubscribe: {UNSUBSCRIBE_URL}"
        ),
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #1e293b;">Reset your password</h2>
            <p style="color: #475569; font-size: 16px;">
                We received a request to reset the password for your Quizify account.
                Click the button below to choose a new one:
            </p>
            <div style="text-align: center; margin: 32px 0;">
                <a href="{reset_url}"
                   style="background-color: #2563eb; color: white; padding: 12px 32px;
                          text-decoration: none; border-radius: 8px; font-weight: bold;
                          font-size: 16px; display: inline-block;">
                    Reset Password
                </a>
            </div>
            <p style="color: #64748b; font-size: 14px;">
                Or copy and paste this link into your browser:<br>
                <a href="{reset_url}" style="color: #2563eb;">{reset_url}</a>
            </p>
            <p style="color: #94a3b8; font-size: 12px; margin-top: 32px;">
                This link expires in 1 hour. If you didn't request a password reset, you can safely ignore this email — your password won't change.
            </p>
            {_footer_html()}
        </div>
        """
    })
