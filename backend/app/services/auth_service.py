"""
Auth Service for Google OAuth Integration.

Handles Google Calendar OAuth authorization URL generation, token code exchange,
and token persistence to file.
"""

from typing import Dict, Any
from app.core.config import settings
from app.core.exceptions import BadRequestError, ExternalServiceError
from app.core.logging import logger


class AuthService:
    """Service managing Google OAuth flows."""

    @staticmethod
    def get_authorization_url() -> str:
        """Generates Google OAuth authorization URL for Calendar scope."""
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise BadRequestError("Google Calendar OAuth credentials not configured in backend settings.")

        try:
            from google_auth_oauthlib.flow import Flow
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                },
                scopes=["https://www.googleapis.com/auth/calendar"],
            )
            flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

            authorization_url, _ = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
            )
            return authorization_url
        except BadRequestError:
            raise
        except Exception as e:
            logger.error(f"Google OAuth initialization failed: {e}")
            raise ExternalServiceError(f"Google OAuth initialization failed: {e}") from e

    @staticmethod
    def handle_oauth_callback(code: str) -> Dict[str, str]:
        """Exchanges authorization code for tokens and saves to token.json."""
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise BadRequestError("Google credentials missing in configuration.")

        try:
            from google_auth_oauthlib.flow import Flow
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                },
                scopes=["https://www.googleapis.com/auth/calendar"],
            )
            flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

            flow.fetch_token(code=code)
            credentials = flow.credentials

            with open(settings.TOKEN_FILE_PATH, "w") as token_file:
                token_file.write(credentials.to_json())

            logger.info(f"Saved OAuth credentials to {settings.TOKEN_FILE_PATH}")
            return {
                "status": "success",
                "message": "Google Calendar connected successfully! You can close this window now.",
            }
        except BadRequestError:
            raise
        except Exception as e:
            logger.error(f"Google OAuth callback exchange failed: {e}")
            raise ExternalServiceError(f"Google OAuth callback exchange failed: {e}") from e


auth_service = AuthService()
