from pydantic import BaseModel, Field
from typing import List, Dict, Any


class AgentRequest(BaseModel):
    """Request model for agent endpoint."""
    message: str = Field(..., description="User message", min_length=1)


class DiffRequest(BaseModel):
    """Request model for diff checker endpoint."""
    text1: str = Field(..., description="First text to compare", min_length=1)
    text2: str = Field(..., description="Second text to compare", min_length=1)


class ReviewResponse(BaseModel):
    """Response model for review endpoint."""
    added: List[str] = Field(default_factory=list, description="List of added items")
    removed: List[str] = Field(default_factory=list, description="List of removed items")
    changed: List[str] = Field(default_factory=list, description="List of changed items")


class AgentResponse(BaseModel):
    """Response model for agent endpoint."""
    response: ReviewResponse = Field(..., description="Agent's response")
    tools_used: List[str] = Field(default_factory=list, description="Tools used by the agent")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Full message history")
    more_context: str = Field("", description="Additional context or information from the agent")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    model: str
    available_tools: List[str]
