"""
Email service for sending transactional emails.
Supports SendGrid and other email providers.
"""
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import aiohttp
from src.config import settings
from src.logging_config import get_logger

logger = get_logger(__name__)


class EmailProvider(ABC):
    """Abstract base class for email providers."""

    @abstractmethod
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """Send email via provider."""
        pass


class SendGridProvider(EmailProvider):
    """SendGrid email provider implementation."""

    def __init__(self, api_key: str, from_email: str):
        """
        Initialize SendGrid provider.

        Args:
            api_key: SendGrid API key
            from_email: From email address
        """
        self.api_key = api_key
        self.from_email = from_email
        self.api_url = "https://api.sendgrid.com/v3/mail/send"

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """
        Send email via SendGrid API.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)

        Returns:
            True if email sent successfully
        """
        payload = {
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "subject": subject,
                }
            ],
            "from": {"email": self.from_email},
            "content": [
                {
                    "type": "text/html",
                    "value": html_content,
                }
            ],
        }

        if text_content:
            payload["content"].insert(
                0,
                {
                    "type": "text/plain",
                    "value": text_content,
                },
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                ) as response:
                    if response.status == 202:
                        logger.info(
                            "Email sent via SendGrid",
                            extra={"to": to_email, "subject": subject},
                        )
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(
                            "SendGrid email failed",
                            extra={
                                "status": response.status,
                                "error": error_text,
                                "to": to_email,
                            },
                        )
                        return False

        except Exception as exception:
            logger.error(
                "Failed to send email via SendGrid",
                exc_info=True,
                extra={"to": to_email, "exception": str(exception)},
            )
            return False


class ConsoleEmailProvider(EmailProvider):
    """Console email provider for development (logs to console instead of sending)."""

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """
        Log email to console instead of sending.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)

        Returns:
            Always True (for development)
        """
        logger.info(
            "EMAIL (Console Mode)",
            extra={
                "to": to_email,
                "subject": subject,
                "html_preview": html_content[:100],
                "text_preview": text_content[:100] if text_content else None,
            },
        )
        print("\n" + "=" * 80)
        print(f"TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print("-" * 80)
        print(text_content or html_content)
        print("=" * 80 + "\n")
        return True


class EmailService:
    """Service for sending transactional emails."""

    def __init__(self):
        """Initialize email service with configured provider."""
        self.provider = self._get_provider()

    def _get_provider(self) -> EmailProvider:
        """
        Get configured email provider.

        Returns:
            EmailProvider instance
        """
        if settings.app_env == "development" or not settings.sendgrid_api_key:
            logger.info("Using console email provider (development mode)")
            return ConsoleEmailProvider()

        if settings.email_provider == "sendgrid" and settings.sendgrid_api_key:
            logger.info("Using SendGrid email provider")
            return SendGridProvider(
                api_key=settings.sendgrid_api_key,
                from_email=settings.email_from,
            )

        # Default to console provider if no valid configuration
        logger.warning("No valid email provider configured, using console provider")
        return ConsoleEmailProvider()

    async def send_verification_email(
        self,
        to_email: str,
        verification_token: str,
    ) -> bool:
        """
        Send email verification email.

        Args:
            to_email: User's email address
            verification_token: Verification token

        Returns:
            True if email sent successfully
        """
        # In production, this would be the actual frontend URL
        verification_url = f"http://localhost:3000/verify-email?token={verification_token}"

        subject = "Verify your CodeMentor account"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #0066CC; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{
                    display: inline-block;
                    padding: 12px 24px;
                    background-color: #0066CC;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to CodeMentor!</h1>
                </div>
                <div class="content">
                    <p>Hi there,</p>
                    <p>Thank you for signing up for CodeMentor. Please verify your email address to activate your account.</p>
                    <p style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email Address</a>
                    </p>
                    <p>Or copy and paste this link into your browser:</p>
                    <p><a href="{verification_url}">{verification_url}</a></p>
                    <p>This link will expire in 24 hours.</p>
                    <p>If you didn't create an account, you can safely ignore this email.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 CodeMentor. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Welcome to CodeMentor!

        Thank you for signing up. Please verify your email address to activate your account.

        Click here to verify: {verification_url}

        This link will expire in 24 hours.

        If you didn't create an account, you can safely ignore this email.

        ---
        CodeMentor Team
        """

        return await self.provider.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
        )

    async def send_password_reset_email(
        self,
        to_email: str,
        reset_token: str,
    ) -> bool:
        """
        Send password reset email.

        Args:
            to_email: User's email address
            reset_token: Password reset token

        Returns:
            True if email sent successfully
        """
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}"

        subject = "Reset your CodeMentor password"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #0066CC; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{
                    display: inline-block;
                    padding: 12px 24px;
                    background-color: #0066CC;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                .warning {{ background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset Request</h1>
                </div>
                <div class="content">
                    <p>Hi,</p>
                    <p>We received a request to reset your CodeMentor password.</p>
                    <p style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </p>
                    <p>Or copy and paste this link into your browser:</p>
                    <p><a href="{reset_url}">{reset_url}</a></p>
                    <div class="warning">
                        <strong>Important:</strong> This link will expire in 1 hour for security reasons.
                    </div>
                    <p>If you didn't request a password reset, please ignore this email. Your password will remain unchanged.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 CodeMentor. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Password Reset Request

        We received a request to reset your CodeMentor password.

        Click here to reset your password: {reset_url}

        This link will expire in 1 hour for security reasons.

        If you didn't request a password reset, please ignore this email. Your password will remain unchanged.

        ---
        CodeMentor Team
        """

        return await self.provider.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
        )

    async def send_welcome_email(self, to_email: str, name: str) -> bool:
        """
        Send welcome email after email verification.

        Args:
            to_email: User's email address
            name: User's name

        Returns:
            True if email sent successfully
        """
        subject = "Welcome to CodeMentor - Let's start coding!"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #0066CC; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{
                    display: inline-block;
                    padding: 12px 24px;
                    background-color: #0066CC;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                ul {{ list-style-type: none; padding-left: 0; }}
                li {{ padding: 8px 0; padding-left: 20px; }}
                li:before {{ content: "✓ "; color: #0066CC; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to CodeMentor, {name}!</h1>
                </div>
                <div class="content">
                    <p>Your email has been verified successfully. You're all set to begin your coding journey!</p>
                    <h3>What's next?</h3>
                    <ul>
                        <li>Complete your onboarding interview to personalize your learning experience</li>
                        <li>Get your first daily coding exercise</li>
                        <li>Chat with your AI tutor for guidance and support</li>
                        <li>Join community study groups</li>
                        <li>Connect with a mentor</li>
                    </ul>
                    <p style="text-align: center;">
                        <a href="http://localhost:3000/dashboard" class="button">Get Started</a>
                    </p>
                    <p>We're excited to help you achieve your coding goals!</p>
                </div>
                <div class="footer">
                    <p>&copy; 2025 CodeMentor. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Welcome to CodeMentor, {name}!

        Your email has been verified successfully. You're all set to begin your coding journey!

        What's next?
        • Complete your onboarding interview to personalize your learning experience
        • Get your first daily coding exercise
        • Chat with your AI tutor for guidance and support
        • Join community study groups
        • Connect with a mentor

        Get started: http://localhost:3000/dashboard

        We're excited to help you achieve your coding goals!

        ---
        CodeMentor Team
        """

        return await self.provider.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
        )


# Global email service instance
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """
    Get the global email service instance.

    Returns:
        EmailService instance
    """
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
