"""
Pydantic Schemas for Timer and Notification Endpoints.
"""

from pydantic import BaseModel, Field


class TimerRequest(BaseModel):
    title: str = Field(..., description="Timer label or description")
    seconds: int = Field(..., description="Duration in seconds")


class TimerResponse(BaseModel):
    status: str = "ok"
    message: str
