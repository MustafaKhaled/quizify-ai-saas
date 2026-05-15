import os
import resend
from dotenv import load_dotenv

from security import make_unsubscribe_token

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

# Send FROM a real, monitored mailbox (not a no-reply alias). Gmail / Outlook
# weight sender reputation heavily on whether the from-address can actually
# receive mail and shows interaction (replies, opens). Using `hello@` as the
# from-address makes the `reply_to` header redundant for most clients —
# replies land in the same inbox naturally.
EMAIL_FROM = os.getenv("EMAIL_FROM", "Quizify AI <hello@quizifyai.app>")
REPLY_TO = os.getenv("EMAIL_REPLY_TO", "hello@quizifyai.app")
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:3000")
# Marketing site — reset-password lives here since users are signed out when they click the email link.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")
# Backend URL is what the List-Unsubscribe header points at, because mailbox
# providers expect to POST directly per RFC 8058 (One-Click). The marketing
# page handles the user-facing confirmation flow.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
COMPANY_ADDRESS = os.getenv("COMPANY_ADDRESS", "Quizify AI , Vienna, Austria")
SUPPORT_EMAIL = os.getenv("EMAIL_REPLY_TO", "hello@quizifyai.app")
HELP_CENTER_URL = f"{FRONTEND_URL}/faq"


def _unsubscribe_url(to_email: str) -> str:
    """User-facing footer link — points at the marketing page, which renders
    a confirm UI before calling the backend POST."""
    token = make_unsubscribe_token(to_email)
    return f"{FRONTEND_URL}/unsubscribe?token={token}"


def _one_click_unsubscribe_url(to_email: str) -> str:
    """Mailbox-provider-facing URL for One-Click POST. Points directly at the
    backend so providers don't have to bounce through the marketing site."""
    token = make_unsubscribe_token(to_email)
    return f"{BACKEND_URL}/unsubscribe?token={token}"


def _footer_html(to_email: str) -> str:
    # The contact line above the address/unsubscribe block matters for
    # deliverability — Gmail/Outlook reduce spam-folder placement when emails
    # show clear, real contact paths. Real human inbox + help-center link
    # also lowers the "Report spam" rate when users have a question.
    unsubscribe_url = _unsubscribe_url(to_email)
    return f"""
    <p style="color: #64748b; font-size: 12px; margin-top: 32px; text-align: center;">
        Questions? Contact us at
        <a href="mailto:{SUPPORT_EMAIL}" style="color: #2563eb;">{SUPPORT_EMAIL}</a>
        or visit our
        <a href="{HELP_CENTER_URL}" style="color: #2563eb;">Help Center</a>.
    </p>
    <p style="color: #94a3b8; font-size: 10px; margin-top: 12px; text-align: center;">
        {COMPANY_ADDRESS} | <a href="{unsubscribe_url}" style="color: #94a3b8;">Unsubscribe</a>
    </p>
    """


def _list_unsubscribe_headers(to_email: str) -> dict:
    """Headers spam filters check to identify legitimate transactional/list mail.
    Per RFC 8058, the List-Unsubscribe URL should accept POST for One-Click —
    we point it at the backend endpoint rather than the marketing page."""
    one_click_url = _one_click_unsubscribe_url(to_email)
    return {
        "List-Unsubscribe": f"<{one_click_url}>, <mailto:{REPLY_TO}?subject=unsubscribe>",
        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
    }


def send_verification_email(to_email: str, token: str):
    verification_url = f"{DASHBOARD_URL}/verify-email?token={token}"

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": [to_email],
        "reply_to": REPLY_TO,
        "subject": "Verify your email - Quizify",
        "headers": _list_unsubscribe_headers(to_email),
        "text": (
            f"Welcome to Quizify!\n\n"
            f"Verify your email by visiting:\n{verification_url}\n\n"
            f"This link expires in 24 hours. If you didn't create an account, you can ignore this email.\n\n"
            f"{COMPANY_ADDRESS}\nUnsubscribe: {_unsubscribe_url(to_email)}"
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
            {_footer_html(to_email)}
        </div>
        """
    })


def send_welcome_email(to_email: str, name: str | None = None):
    """One-shot welcome email — sent after Google OAuth first signup OR after
    successful email verification. Both paths produce the same "user is now
    fully onboarded" state, so they share this email.

    The copy mirrors the new marketing positioning ("Pass it. Or master it.")
    and gives the user a concrete first action: pick their subjects in
    onboarding. Mentions the trial allowance so they know what's included.
    """
    greeting = f"Hi {name}," if name else "Welcome,"
    onboarding_url = f"{DASHBOARD_URL}/onboarding"
    library_url = f"{DASHBOARD_URL}/subjects"

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": [to_email],
        "reply_to": REPLY_TO,
        "subject": "Welcome to Quizify — pick your first track",
        "headers": _list_unsubscribe_headers(to_email),
        "text": (
            f"{greeting}\n\n"
            f"You're in. Quizify is built around two outcomes: passing the certification "
            f"you're studying for, and finding the topics you don't actually know yet "
            f"(so you can stop wasting study hours on what you've already learned).\n\n"
            f"Your free 7-day trial includes:\n"
            f"  • 3 practice quizzes on any curated track\n"
            f"  • 1 Goethe-B1 Hören mock exam (audio + transcripts)\n"
            f"  • Full per-topic weakness analytics on every quiz\n\n"
            f"Get started:\n"
            f"  1. Pick the certifications or grammar levels you're preparing for: {onboarding_url}\n"
            f"  2. Generate your first quiz — fresh questions in seconds\n"
            f"  3. Read your weakness map — the dashboard tells you what to study next\n\n"
            f"Available tracks: PMP, AWS Cloud Practitioner, Goethe German A1 / A2 / B1, "
            f"Goethe-B1 Hören. New tracks roll out regularly.\n\n"
            f"Reply to this email if you get stuck — a real person reads it.\n\n"
            f"— The Quizify team\n\n"
            f"{COMPANY_ADDRESS}\nUnsubscribe: {_unsubscribe_url(to_email)}"
        ),
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #1e293b; font-size: 24px; margin-bottom: 8px;">Pass it. Or master it.</h2>
            <p style="color: #475569; font-size: 16px; line-height: 1.5;">
                {greeting} you're in. Quizify is built around two outcomes:
                <strong>passing the certification you're studying for</strong>,
                and <strong>finding the topics you don't actually know yet</strong> —
                so you can stop wasting study hours on what you've already learned.
            </p>

            <div style="background: #f1f5f9; border-radius: 12px; padding: 20px; margin: 24px 0;">
                <p style="color: #1e293b; font-weight: bold; margin: 0 0 12px 0; font-size: 14px;">
                    Your 7-day free trial includes
                </p>
                <ul style="color: #475569; font-size: 14px; margin: 0; padding-left: 20px; line-height: 1.7;">
                    <li>3 practice quizzes on any curated track</li>
                    <li>1 Goethe-B1 Hören mock exam (audio + transcripts)</li>
                    <li>Full per-topic weakness analytics on every quiz</li>
                </ul>
            </div>

            <div style="text-align: center; margin: 32px 0;">
                <a href="{onboarding_url}"
                   style="background-color: #2563eb; color: white; padding: 12px 32px;
                          text-decoration: none; border-radius: 8px; font-weight: bold;
                          font-size: 16px; display: inline-block;">
                    Pick your first tracks
                </a>
            </div>

            <p style="color: #475569; font-size: 14px; line-height: 1.7;">
                <strong style="color: #1e293b;">Available now:</strong> PMP, AWS Cloud Practitioner,
                Goethe German A1 / A2 / B1, Goethe-B1 Hören. New tracks roll out regularly.
            </p>

            <p style="color: #475569; font-size: 14px; line-height: 1.7;">
                <strong style="color: #1e293b;">How a typical session goes:</strong>
            </p>
            <ol style="color: #475569; font-size: 14px; line-height: 1.7; padding-left: 20px;">
                <li>Pick a topic from your track and generate a quiz in seconds.</li>
                <li>Run the timer — it matches the duration of the real exam.</li>
                <li>Read your weakness map — the dashboard ranks the chapters most worth your next study session.</li>
            </ol>

            <p style="color: #475569; font-size: 14px; margin-top: 24px;">
                Reply to this email if you get stuck — a real person reads it.
            </p>

            <p style="color: #94a3b8; font-size: 13px; margin-top: 32px;">
                — The Quizify team
            </p>

            <p style="color: #94a3b8; font-size: 12px; margin-top: 16px;">
                Manage your library anytime at
                <a href="{library_url}" style="color: #2563eb;">your dashboard</a>.
            </p>

            {_footer_html(to_email)}
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
        "headers": _list_unsubscribe_headers(to_email),
        "text": (
            f"Reset your Quizify password\n\n"
            f"We received a request to reset the password for your account. "
            f"Open this link in your browser to choose a new one:\n{reset_url}\n\n"
            f"This link expires in 1 hour. If you didn't request a password reset, "
            f"you can safely ignore this email — your password won't change.\n\n"
            f"{COMPANY_ADDRESS}\nUnsubscribe: {_unsubscribe_url(to_email)}"
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
            {_footer_html(to_email)}
        </div>
        """
    })
