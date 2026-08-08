"""
Google OAuth Integration API Router with Dependency Injection.
"""

from fastapi import APIRouter, Depends
from app.schemas.auth import OAuthConnectResponse, OAuthCallbackResponse
from app.services.auth_service import AuthService
from app.api.deps import get_auth_service

router = APIRouter(tags=["Authentication & OAuth"])


@router.get("/google/connect", response_model=OAuthConnectResponse)
def google_connect(
    a_service: AuthService = Depends(get_auth_service),
):
    """Generates Google OAuth authorization URL for Calendar scope."""
    url = a_service.get_authorization_url()
    return {"authorization_url": url}


@router.get("/oauth2callback", response_model=OAuthCallbackResponse)
def oauth2callback(
    code: str,
    a_service: AuthService = Depends(get_auth_service),
):
    """Google OAuth callback code exchange handler."""
    result = a_service.handle_oauth_callback(code)
    return result
