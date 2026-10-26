from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query, status
from app.schemas import (
    TicketCreate,
    TicketPriority,
    TicketResponse,
    TicketStatus,
    TicketUpdate,
)

app = FastAPI(
    title="AI Helpdesk Copilot",
    description="API for managing IT support tickets",
    version="0.1.0",
)

# Temporary in-memory storage.
# PostgreSQL will replace this in a later stage.
tickets: list[TicketResponse] = []


@app.get("/")
def home():
    return {"message": "AI Helpdesk Copilot API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


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
):
    filtered_tickets = tickets

    if ticket_status is not None:
        filtered_tickets = [
            ticket
            for ticket in filtered_tickets
            if ticket.status == ticket_status
        ]

    if ticket_priority is not None:
        filtered_tickets = [
            ticket
            for ticket in filtered_tickets
            if ticket.priority == ticket_priority
        ]

    return filtered_tickets


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ticket not found",
    )
    filtered_tickets = tickets

    if ticket_status is not None:
        filtered_tickets = [
            ticket
            for ticket in filtered_tickets
            if ticket.status == ticket_status
        ]

    if ticket_priority is not None:
        filtered_tickets = [
            ticket
            for ticket in filtered_tickets
            if ticket.priority == ticket_priority
        ]

    return filtered_tickets


@app.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(ticket_data: TicketCreate):
    new_ticket = TicketResponse(
        id=len(tickets) + 1,
        title=ticket_data.title,
        description=ticket_data.description,
        category=ticket_data.category,
        priority=ticket_data.priority,
        status=TicketStatus.OPEN,
        created_at=datetime.now(timezone.utc),
    )

    tickets.append(new_ticket)
    return new_ticket


@app.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, updates: TicketUpdate):
    # 1. Find the ticket and remember its position.
    for index, existing_ticket in enumerate(tickets):
        if existing_ticket.id == ticket_id:
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    # 2. Extract only the fields supplied in the request.
    update_data = updates.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    # 3. Reject requests that contain no update fields.
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update",
        )

    # 4. Create the updated ticket.
    updated_ticket = existing_ticket.model_copy(update=update_data)

    # 5. Replace the old ticket in temporary storage.
    tickets[index] = updated_ticket

    # 6. Return the updated ticket.
    return updated_ticket