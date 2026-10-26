from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TicketStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"


class TicketPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5, max_length=2000)
    category: str = Field(min_length=2, max_length=60)
    priority: TicketPriority


class TicketUpdate(BaseModel):
    status: TicketStatus | None = None
    priority: TicketPriority | None = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime