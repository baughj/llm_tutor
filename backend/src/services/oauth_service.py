"""
OAuth service for GitHub and Google authentication.
Handles OAuth flows, token exchange, and user profile retrieval.
"""
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import secrets
import aiohttp
from src.config import settings
from src.logging_config import get_logger
from src.middleware.error_handler import APIError
from src.utils.redis_client import get_redis

logger = get_logger(__name__)


class OAuthService:
    """Service for OAuth authentication with multiple providers."""

    # OAuth endpoints
    GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_USER_URL = "https://api.github.com/user"
    GITHUB_EMAIL_URL = "https://api.github.com/user/emails"

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    @staticmethod
    async def generate_oauth_state(provider: str) -> str:
        """
        Generate and store OAuth state parameter for CSRF protection.

        Args:
            provider: OAuth provider (github or google)

        Returns:
            State parameter
        """
        state = secrets.token_urlsafe(32)

        # Store state in Redis with 10-minute expiration
        redis_manager = get_redis()
        key = f"oauth_state:{state}"
        await redis_manager.set_cache(
            key,
            {"provider": provider, "created_at": "now"},
            expiration=600,  # 10 minutes
        )

        logger.info(
            "OAuth state generated",
            extra={"provider": provider, "state": state[:10] + "..."},
        )

        return state

    @staticmethod
    async def verify_oauth_state(state: str, expected_provider: str) -> bool:
        """
        Verify OAuth state parameter.

        Args:
            state: State parameter to verify
            expected_provider: Expected OAuth provider

        Returns:
            True if state is valid

        Raises:
            APIError: If state is invalid
        """
        redis_manager = get_redis()
        key = f"oauth_state:{state}"
        data = await redis_manager.get_cache(key)

        if not data:
            logger.warning("Invalid or expired OAuth state", extra={"state": state[:10] + "..."})
            raise APIError("Invalid OAuth state parameter", status_code=400)

        if data.get("provider") != expected_provider:
            logger.warning(
                "OAuth provider mismatch",
                extra={
                    "expected": expected_provider,
                    "actual": data.get("provider"),
                },
            )
            raise APIError("OAuth provider mismatch", status_code=400)

        # Delete state after verification (one-time use)
        await redis_manager.delete_cache(key)

        logger.info("OAuth state verified", extra={"provider": expected_provider})
        return True

    @staticmethod
    def get_github_authorization_url(state: str, redirect_uri: str) -> str:
        """
        Generate GitHub OAuth authorization URL.

        Args:
            state: CSRF state parameter
            redirect_uri: OAuth callback URL

        Returns:
            Authorization URL
        """
        params = {
            "client_id": settings.github_client_id,
            "redirect_uri": redirect_uri,
            "scope": "read:user user:email",
            "state": state,
        }

        url = f"{OAuthService.GITHUB_AUTH_URL}?{urlencode(params)}"
        logger.info("GitHub authorization URL generated")
        return url

    @staticmethod
    async def exchange_github_code(code: str, redirect_uri: str) -> str:
        """
        Exchange GitHub authorization code for access token.

        Args:
            code: Authorization code from GitHub
            redirect_uri: OAuth callback URL

        Returns:
            GitHub access token

        Raises:
            APIError: If token exchange fails
        """
        payload = {
            "client_id": settings.github_client_id,
            "client_secret": settings.github_client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }

        headers = {
            "Accept": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    OAuthService.GITHUB_TOKEN_URL,
                    json=payload,
                    headers=headers,
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(
                            "GitHub token exchange failed",
                            extra={"status": response.status, "error": error_text},
                        )
                        raise APIError(
                            "Failed to exchange GitHub code for token",
                            status_code=400,
                        )

                    data = await response.json()
                    access_token = data.get("access_token")

                    if not access_token:
                        logger.error("No access token in GitHub response", extra={"data": data})
                        raise APIError("Invalid GitHub token response", status_code=400)

                    logger.info("GitHub access token obtained")
                    return access_token

        except aiohttp.ClientError as exception:
            logger.error("GitHub token exchange request failed", exc_info=True)
            raise APIError(f"GitHub OAuth error: {str(exception)}", status_code=500)

    @staticmethod
    async def get_github_user_info(access_token: str) -> Dict[str, Any]:
        """
        Get user information from GitHub.

        Args:
            access_token: GitHub access token

        Returns:
            User profile data

        Raises:
            APIError: If request fails
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                # Get user profile
                async with session.get(
                    OAuthService.GITHUB_USER_URL,
                    headers=headers,
                ) as response:
                    if response.status != 200:
                        logger.error(
                            "GitHub user info request failed",
                            extra={"status": response.status},
                        )
                        raise APIError("Failed to get GitHub user info", status_code=400)

                    user_data = await response.json()

                # Get user emails
                async with session.get(
                    OAuthService.GITHUB_EMAIL_URL,
                    headers=headers,
                ) as response:
                    if response.status == 200:
                        emails = await response.json()
                        # Find primary verified email
                        primary_email = next(
                            (e for e in emails if e.get("primary") and e.get("verified")),
                            None,
                        )
                        if primary_email:
                            user_data["email"] = primary_email["email"]

            profile = {
                "github_id": str(user_data["id"]),
                "email": user_data.get("email"),
                "name": user_data.get("name") or user_data.get("login"),
                "avatar_url": user_data.get("avatar_url"),
                "bio": user_data.get("bio"),
            }

            logger.info(
                "GitHub user info retrieved",
                extra={"github_id": profile["github_id"], "email": profile.get("email")},
            )

            return profile

        except aiohttp.ClientError as exception:
            logger.error("GitHub user info request failed", exc_info=True)
            raise APIError(f"GitHub API error: {str(exception)}", status_code=500)

    @staticmethod
    def get_google_authorization_url(state: str, redirect_uri: str) -> str:
        """
        Generate Google OAuth authorization URL.

        Args:
            state: CSRF state parameter
            redirect_uri: OAuth callback URL

        Returns:
            Authorization URL
        """
        params = {
            "client_id": settings.google_client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }

        url = f"{OAuthService.GOOGLE_AUTH_URL}?{urlencode(params)}"
        logger.info("Google authorization URL generated")
        return url

    @staticmethod
    async def exchange_google_code(code: str, redirect_uri: str) -> str:
        """
        Exchange Google authorization code for access token.

        Args:
            code: Authorization code from Google
            redirect_uri: OAuth callback URL

        Returns:
            Google access token

        Raises:
            APIError: If token exchange fails
        """
        payload = {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    OAuthService.GOOGLE_TOKEN_URL,
                    data=payload,
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(
                            "Google token exchange failed",
                            extra={"status": response.status, "error": error_text},
                        )
                        raise APIError(
                            "Failed to exchange Google code for token",
                            status_code=400,
                        )

                    data = await response.json()
                    access_token = data.get("access_token")

                    if not access_token:
                        logger.error("No access token in Google response", extra={"data": data})
                        raise APIError("Invalid Google token response", status_code=400)

                    logger.info("Google access token obtained")
                    return access_token

        except aiohttp.ClientError as exception:
            logger.error("Google token exchange request failed", exc_info=True)
            raise APIError(f"Google OAuth error: {str(exception)}", status_code=500)

    @staticmethod
    async def get_google_user_info(access_token: str) -> Dict[str, Any]:
        """
        Get user information from Google.

        Args:
            access_token: Google access token

        Returns:
            User profile data

        Raises:
            APIError: If request fails
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    OAuthService.GOOGLE_USER_URL,
                    headers=headers,
                ) as response:
                    if response.status != 200:
                        logger.error(
                            "Google user info request failed",
                            extra={"status": response.status},
                        )
                        raise APIError("Failed to get Google user info", status_code=400)

                    user_data = await response.json()

            profile = {
                "google_id": user_data["id"],
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "avatar_url": user_data.get("picture"),
                "email_verified": user_data.get("verified_email", False),
            }

            logger.info(
                "Google user info retrieved",
                extra={"google_id": profile["google_id"], "email": profile.get("email")},
            )

            return profile

        except aiohttp.ClientError as exception:
            logger.error("Google user info request failed", exc_info=True)
            raise APIError(f"Google API error: {str(exception)}", status_code=500)


def get_oauth_service() -> OAuthService:
    """
    Get OAuth service instance.

    Returns:
        OAuthService instance
    """
    return OAuthService()
