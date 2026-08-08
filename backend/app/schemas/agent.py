"""
Pydantic Schemas for Agent Endpoints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    goal: str = Field(..., description="The user's goal or prompt for the agent")
    language: str = Field(default="english", description="Target output language: english or hinglish")
    mode: str = Field(default="normal", description="Agent execution mode: normal or ask")
    history: List[Dict[str, Any]] = Field(default_factory=list, description="Recent conversation history")


class AgentStartResponse(BaseModel):
    run_id: str = Field(..., description="Unique UUID identifier for the agent run")
    status: str = Field(default="started")


class StepRecord(BaseModel):
    step: str
    tool_used: str
    input: Any
    output: Any


class AgentStatusResponse(BaseModel):
    goal: Optional[str] = None
    plan: List[str] = Field(default_factory=list)
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    final_result: Optional[str] = None
    self_check: Optional[str] = None
    sentiment: str = "neutral"
    is_debating: bool = False
    debate_a: str = ""
    debate_b: str = ""
    status: str = "running"
    error: Optional[str] = None


class SuggestionRequest(BaseModel):
    history: List[Dict[str, Any]] = Field(default_factory=list)
    language: str = Field(default="english")


class SuggestionItem(BaseModel):
    text: str
    prompt: str


class SuggestionResponse(BaseModel):
    suggestions: List[SuggestionItem] = Field(default_factory=list)
