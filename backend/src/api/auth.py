"""
Authentication API endpoints.
Handles user registration, login, OAuth, and session management.
"""
from quart import Blueprint, request, jsonify, redirect
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.logging_config import get_logger
from src.middleware.error_handler import APIError
from src.middleware.auth_middleware import require_auth, get_current_user_id
from src.services.auth_service import AuthService
from src.services.email_service import get_email_service
from src.services.oauth_service import OAuthService
from src.models.user import User, UserRole
from src.models.base import get_session

logger = get_logger(__name__)
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
async def register() -> Dict[str, Any]:
    """
    Register a new user with email and password.

    Request Body:
        {
            "email": "user@example.com",
            "password": "secure_password",
            "name": "User Name"
        }

    Returns:
        JSON response with user data and message
    """
    data = await request.get_json()

    # Validate required fields
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    name = data.get("name", "").strip()

    if not email or not password or not name:
        raise APIError(
            "Email, password, and name are required",
            status_code=400,
        )

    # Validate email format
    AuthService.validate_email(email)

    # Validate password requirements
    AuthService.validate_password(password)

    # Hash password
    password_hash = AuthService.hash_password(password)

    # Generate email verification token
    verification_token = AuthService.generate_verification_token()

    # Create user in database
    async with get_session() as session:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.email == email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.warning(
                "Registration attempt with existing email",
                extra={"email": email},
            )
            raise APIError(
                "User with this email already exists",
                status_code=409,
            )

        # Create new user
        new_user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            role=UserRole.STUDENT,
            email_verified=False,
            is_active=True,
        )

        session.add(new_user)

        try:
            await session.commit()
            await session.refresh(new_user)

            logger.info(
                "User registered successfully",
                extra={"user_id": new_user.id, "email": email},
            )

            # Store verification token in Redis
            await AuthService.store_verification_token(email, verification_token)

            # Send verification email
            email_service = get_email_service()
            await email_service.send_verification_email(email, verification_token)

            return jsonify({
                "message": "Registration successful. Please check your email to verify your account.",
                "user": {
                    "id": new_user.id,
                    "email": new_user.email,
                    "name": new_user.name,
                    "email_verified": new_user.email_verified,
                },
            }), 201

        except IntegrityError as exception:
            await session.rollback()
            logger.error("Database integrity error during registration", exc_info=True)
            raise APIError(
                "User with this email already exists",
                status_code=409,
            )


@auth_bp.route("/login", methods=["POST"])
async def login() -> Dict[str, Any]:
    """
    Login with email and password.

    Request Body:
        {
            "email": "user@example.com",
            "password": "secure_password"
        }

    Returns:
        JSON response with JWT tokens
    """
    data = await request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        raise APIError("Email and password are required", status_code=400)

    # Get user from database
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user or not user.password_hash:
            logger.warning("Login attempt with invalid credentials", extra={"email": email})
            raise APIError("Invalid email or password", status_code=401)

        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            logger.warning("Login attempt with wrong password", extra={"email": email})
            raise APIError("Invalid email or password", status_code=401)

        # Check if user is active
        if not user.is_active:
            logger.warning("Login attempt for inactive user", extra={"email": email})
            raise APIError("Account is inactive. Please contact support.", status_code=403)

        # Generate token pair
        tokens = AuthService.generate_token_pair(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
        )

        # Create session in Redis
        await AuthService.create_session(
            user_id=user.id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user_data={
                "name": user.name,
                "email_verified": user.email_verified,
            },
        )

        # Update last login timestamp
        user.last_login = datetime.utcnow()
        await session.commit()

        logger.info("User logged in successfully", extra={"user_id": user.id, "email": email})

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value,
                "email_verified": user.email_verified,
            },
            **tokens,
        }), 200


@auth_bp.route("/logout", methods=["POST"])
@require_auth
async def logout() -> Dict[str, Any]:
    """
    Logout and invalidate session.

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        JSON response confirming logout
    """
    user_id = get_current_user_id()

    # Get token from header
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split()[1] if len(auth_header.split()) == 2 else None

    if token:
        # Invalidate session in Redis
        await AuthService.invalidate_session(user_id, token)

    logger.info("User logged out successfully", extra={"user_id": user_id})

    return jsonify({
        "message": "Logout successful"
    }), 200


@auth_bp.route("/oauth/github", methods=["GET"])
async def oauth_github() -> Dict[str, Any]:
    """
    Initiate GitHub OAuth flow.

    Returns:
        Redirect to GitHub authorization URL
    """
    # Generate OAuth state for CSRF protection
    state = await OAuthService.generate_oauth_state("github")

    # Build redirect URI (in production, this should come from config)
    redirect_uri = "http://localhost:5000/api/v1/auth/oauth/github/callback"

    # Get authorization URL
    auth_url = OAuthService.get_github_authorization_url(state, redirect_uri)

    logger.info("GitHub OAuth flow initiated", extra={"state": state[:10] + "..."})

    # Redirect to GitHub
    return redirect(auth_url)


@auth_bp.route("/oauth/github/callback", methods=["GET"])
async def oauth_github_callback() -> Dict[str, Any]:
    """
    Handle GitHub OAuth callback.

    Query Parameters:
        code: Authorization code from GitHub
        state: State parameter for CSRF protection

    Returns:
        Redirect to frontend with tokens
    """
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        raise APIError("Missing OAuth parameters", status_code=400)

    # Verify state parameter
    await OAuthService.verify_oauth_state(state, "github")

    # Exchange code for access token
    redirect_uri = "http://localhost:5000/api/v1/auth/oauth/github/callback"
    github_access_token = await OAuthService.exchange_github_code(code, redirect_uri)

    # Get user info from GitHub
    github_profile = await OAuthService.get_github_user_info(github_access_token)

    if not github_profile.get("email"):
        raise APIError(
            "GitHub account must have a verified email address",
            status_code=400,
        )

    # Create or update user in database
    async with get_session() as session:
        # Check if user exists with this GitHub ID
        result = await session.execute(
            select(User).where(User.github_id == github_profile["github_id"])
        )
        user = result.scalar_one_or_none()

        if not user:
            # Check if user exists with this email
            result = await session.execute(
                select(User).where(User.email == github_profile["email"])
            )
            user = result.scalar_one_or_none()

            if user:
                # Link GitHub account to existing user
                user.github_id = github_profile["github_id"]
                user.oauth_provider = "github"
                if not user.avatar_url:
                    user.avatar_url = github_profile.get("avatar_url")
                logger.info("GitHub account linked to existing user", extra={"user_id": user.id})
            else:
                # Create new user
                user = User(
                    email=github_profile["email"],
                    github_id=github_profile["github_id"],
                    oauth_provider="github",
                    name=github_profile["name"],
                    avatar_url=github_profile.get("avatar_url"),
                    bio=github_profile.get("bio"),
                    email_verified=True,  # GitHub emails are verified
                    role=UserRole.STUDENT,
                    is_active=True,
                )
                session.add(user)
                logger.info("New user created via GitHub OAuth", extra={"email": github_profile["email"]})

        await session.commit()
        await session.refresh(user)

        # Generate JWT tokens
        tokens = AuthService.generate_token_pair(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
        )

        # Create session
        await AuthService.create_session(
            user_id=user.id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user_data={
                "name": user.name,
                "email_verified": user.email_verified,
            },
        )

        # Update last login
        user.last_login = datetime.utcnow()
        await session.commit()

        logger.info("GitHub OAuth successful", extra={"user_id": user.id})

        # Redirect to frontend with tokens
        # In production, encode tokens in URL or use a different flow
        frontend_url = f"http://localhost:3000/auth/callback?access_token={tokens['access_token']}&refresh_token={tokens['refresh_token']}"
        return redirect(frontend_url)


@auth_bp.route("/oauth/google", methods=["GET"])
async def oauth_google() -> Dict[str, Any]:
    """
    Initiate Google OAuth flow.

    Returns:
        Redirect to Google authorization URL
    """
    # Generate OAuth state for CSRF protection
    state = await OAuthService.generate_oauth_state("google")

    # Build redirect URI
    redirect_uri = "http://localhost:5000/api/v1/auth/oauth/google/callback"

    # Get authorization URL
    auth_url = OAuthService.get_google_authorization_url(state, redirect_uri)

    logger.info("Google OAuth flow initiated", extra={"state": state[:10] + "..."})

    # Redirect to Google
    return redirect(auth_url)


@auth_bp.route("/oauth/google/callback", methods=["GET"])
async def oauth_google_callback() -> Dict[str, Any]:
    """
    Handle Google OAuth callback.

    Query Parameters:
        code: Authorization code from Google
        state: State parameter for CSRF protection

    Returns:
        Redirect to frontend with tokens
    """
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        raise APIError("Missing OAuth parameters", status_code=400)

    # Verify state parameter
    await OAuthService.verify_oauth_state(state, "google")

    # Exchange code for access token
    redirect_uri = "http://localhost:5000/api/v1/auth/oauth/google/callback"
    google_access_token = await OAuthService.exchange_google_code(code, redirect_uri)

    # Get user info from Google
    google_profile = await OAuthService.get_google_user_info(google_access_token)

    if not google_profile.get("email"):
        raise APIError(
            "Google account must have an email address",
            status_code=400,
        )

    # Create or update user in database
    async with get_session() as session:
        # Check if user exists with this Google ID
        result = await session.execute(
            select(User).where(User.google_id == google_profile["google_id"])
        )
        user = result.scalar_one_or_none()

        if not user:
            # Check if user exists with this email
            result = await session.execute(
                select(User).where(User.email == google_profile["email"])
            )
            user = result.scalar_one_or_none()

            if user:
                # Link Google account to existing user
                user.google_id = google_profile["google_id"]
                user.oauth_provider = "google"
                if not user.avatar_url:
                    user.avatar_url = google_profile.get("avatar_url")
                logger.info("Google account linked to existing user", extra={"user_id": user.id})
            else:
                # Create new user
                user = User(
                    email=google_profile["email"],
                    google_id=google_profile["google_id"],
                    oauth_provider="google",
                    name=google_profile["name"],
                    avatar_url=google_profile.get("avatar_url"),
                    email_verified=google_profile.get("email_verified", True),
                    role=UserRole.STUDENT,
                    is_active=True,
                )
                session.add(user)
                logger.info("New user created via Google OAuth", extra={"email": google_profile["email"]})

        await session.commit()
        await session.refresh(user)

        # Generate JWT tokens
        tokens = AuthService.generate_token_pair(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
        )

        # Create session
        await AuthService.create_session(
            user_id=user.id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user_data={
                "name": user.name,
                "email_verified": user.email_verified,
            },
        )

        # Update last login
        user.last_login = datetime.utcnow()
        await session.commit()

        logger.info("Google OAuth successful", extra={"user_id": user.id})

        # Redirect to frontend with tokens
        frontend_url = f"http://localhost:3000/auth/callback?access_token={tokens['access_token']}&refresh_token={tokens['refresh_token']}"
        return redirect(frontend_url)


@auth_bp.route("/refresh", methods=["POST"])
async def refresh_token() -> Dict[str, Any]:
    """
    Refresh access token using refresh token.

    Request Body:
        {
            "refresh_token": "refresh_token_here"
        }

    Returns:
        JSON response with new access token
    """
    data = await request.get_json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        raise APIError("Refresh token is required", status_code=400)

    # Verify refresh token
    payload = AuthService.verify_jwt_token(refresh_token, token_type="refresh")

    # Get user from database to ensure they still exist and are active
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.id == payload["user_id"])
        )
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            logger.warning(
                "Refresh attempt for non-existent or inactive user",
                extra={"user_id": payload["user_id"]},
            )
            raise APIError("Invalid refresh token", status_code=401)

        # Generate new access token
        new_access_token = AuthService.generate_jwt_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type="access",
        )

        # Create new session with the new access token
        await AuthService.create_session(
            user_id=user.id,
            access_token=new_access_token,
            refresh_token=refresh_token,
            user_data={
                "name": user.name,
                "email_verified": user.email_verified,
            },
        )

        logger.info("Access token refreshed", extra={"user_id": user.id})

        return jsonify({
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 86400,  # 24 hours in seconds
        }), 200


@auth_bp.route("/verify-email", methods=["POST"])
async def verify_email() -> Dict[str, Any]:
    """
    Verify user email with verification token.

    Request Body:
        {
            "token": "verification_token"
        }

    Returns:
        JSON response confirming verification
    """
    data = await request.get_json()
    token = data.get("token")

    if not token:
        raise APIError("Verification token is required", status_code=400)

    # Verify token and get email
    email = await AuthService.verify_verification_token(token)

    if not email:
        raise APIError("Invalid or expired verification token", status_code=400)

    # Update user in database
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.error("User not found for email verification", extra={"email": email})
            raise APIError("User not found", status_code=404)

        if user.email_verified:
            logger.info("Email already verified", extra={"user_id": user.id})
            return jsonify({
                "message": "Email already verified"
            }), 200

        # Mark email as verified
        user.email_verified = True
        await session.commit()

        logger.info("Email verified successfully", extra={"user_id": user.id, "email": email})

        # Send welcome email
        email_service = get_email_service()
        await email_service.send_welcome_email(user.email, user.name)

        return jsonify({
            "message": "Email verified successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "email_verified": user.email_verified,
            },
        }), 200


@auth_bp.route("/password-reset", methods=["POST"])
async def request_password_reset() -> Dict[str, Any]:
    """
    Request password reset email.

    Request Body:
        {
            "email": "user@example.com"
        }

    Returns:
        JSON response confirming email sent
    """
    data = await request.get_json()
    email = data.get("email", "").strip().lower()

    if not email:
        raise APIError("Email is required", status_code=400)

    AuthService.validate_email(email)

    # Check if user exists
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        # Always return success to prevent email enumeration
        # Don't reveal whether user exists or not
        if not user:
            logger.info("Password reset requested for non-existent email", extra={"email": email})
            return jsonify({
                "message": "If an account with that email exists, a password reset link has been sent."
            }), 200

        # Generate reset token
        reset_token = AuthService.generate_verification_token()

        # Store token in Redis (1 hour expiration)
        await AuthService.store_password_reset_token(email, reset_token, expiration=3600)

        # Send reset email
        email_service = get_email_service()
        await email_service.send_password_reset_email(email, reset_token)

        logger.info("Password reset email sent", extra={"user_id": user.id, "email": email})

        return jsonify({
            "message": "If an account with that email exists, a password reset link has been sent."
        }), 200


@auth_bp.route("/password-reset/confirm", methods=["POST"])
async def confirm_password_reset() -> Dict[str, Any]:
    """
    Reset password with token.

    Request Body:
        {
            "token": "reset_token",
            "new_password": "new_secure_password"
        }

    Returns:
        JSON response confirming password reset
    """
    data = await request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        raise APIError("Token and new password are required", status_code=400)

    # Verify token and get email
    email = await AuthService.verify_password_reset_token(token)

    if not email:
        raise APIError("Invalid or expired reset token", status_code=400)

    # Validate new password
    AuthService.validate_password(new_password)

    # Hash new password
    new_password_hash = AuthService.hash_password(new_password)

    # Update user password
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.error("User not found for password reset", extra={"email": email})
            raise APIError("User not found", status_code=404)

        # Update password
        user.password_hash = new_password_hash
        await session.commit()

        logger.info("Password reset successful", extra={"user_id": user.id, "email": email})

        # TODO: Invalidate all existing sessions for this user
        # This would require iterating through Redis sessions or implementing a user session tracking system

        return jsonify({
            "message": "Password reset successful. Please login with your new password."
        }), 200
