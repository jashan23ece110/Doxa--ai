"""
Pydantic Schemas for Auth and Google Integration Endpoints.
"""

from pydantic import BaseModel


class OAuthConnectResponse(BaseModel):
    authorization_url: str


class OAuthCallbackResponse(BaseModel):
    status: str = "success"
    message: str
