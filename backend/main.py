
from pathlib import Path
from backend.logging_config import logger

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Ticket
from backend.schemas import (
    TicketCreate,
    TicketPriority,
    TicketResponse,
    TicketStatus,
    TicketUpdate,
)


# --------------------------------------------------
# Application configuration
# --------------------------------------------------

app = FastAPI(
    title="AI Helpdesk Copilot",
    description="API for managing IT support tickets",
    version="0.1.0",
)

# Locate the frontend directory relative to this file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"

# Serve CSS and JavaScript files.
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


# --------------------------------------------------
# Home and health endpoints
# --------------------------------------------------

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api", include_in_schema=False)
def api_home():
    return {"message": "AI Helpdesk Copilot API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# --------------------------------------------------
# List and filter tickets
# --------------------------------------------------

@app.get("/tickets", response_model=list[TicketResponse])
def list_tickets(
    ticket_status: TicketStatus | None = Query(
        default=None,
        alias="status",
    ),
    ticket_priority: TicketPriority | None = Query(
        default=None,
        alias="priority",
    ),
    db: Session = Depends(get_db),
):
    statement = select(Ticket)

    if ticket_status is not None:
        statement = statement.where(
            Ticket.status == ticket_status.value
        )

    if ticket_priority is not None:
        statement = statement.where(
            Ticket.priority == ticket_priority.value
        )

    statement = statement.order_by(Ticket.id)

    return list(db.scalars(statement).all())


# --------------------------------------------------
# Create a ticket
# --------------------------------------------------

@app.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
):
    new_ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        category=ticket_data.category,
        priority=ticket_data.priority.value,
        status=TicketStatus.OPEN.value,
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    logger.info(
    "Ticket created: id=%s category=%s priority=%s",
    new_ticket.id,
    new_ticket.category,
    new_ticket.priority,
)

    return new_ticket


# --------------------------------------------------
# Retrieve a single ticket
# --------------------------------------------------

@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
    responses={
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Ticket not found"
                    }
                }
            },
        }
    },
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        logger.warning("Ticket not found: id=%s", ticket_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


# --------------------------------------------------
# Update a ticket
# --------------------------------------------------

@app.patch(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
    responses={
        400: {
            "description": "Empty update request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Provide at least one field to update"
                    }
                }
            },
        },
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Ticket not found"
                    }
                }
            },
        },
    },
)
def update_ticket(
    ticket_id: int,
    updates: TicketUpdate,
    db: Session = Depends(get_db),
):
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    update_data = updates.model_dump(
        exclude_unset=True,
        exclude_none=True,
        mode="json",
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update",
        )

    for field, value in update_data.items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    logger.info(
    "Ticket updated: id=%s status=%s priority=%s",
    ticket.id,
    ticket.status,
    ticket.priority,
)
    return ticket
