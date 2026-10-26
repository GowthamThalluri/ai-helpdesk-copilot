const ticketForm = document.getElementById("ticket-form");
const filterForm = document.getElementById("filter-form");
const updateTicketForm = document.getElementById("update-ticket-form");

const formMessage = document.getElementById("form-message");
const listMessage = document.getElementById("list-message");
const updateMessage = document.getElementById("update-message");

const ticketTableBody = document.getElementById("ticket-table-body");
const ticketDetails = document.getElementById("ticket-details");

let selectedTicketId = null;


// Display a message without treating user-provided text as HTML.
function showMessage(element, message, isError = false) {
    element.textContent = message;
    element.style.color = isError ? "#b91c1c" : "#64748b";
}


// Read an API error response.
async function getErrorMessage(response) {
    try {
        const data = await response.json();

        if (typeof data.detail === "string") {
            return data.detail;
        }
    } catch {
        // The server did not return JSON.
    }

    return `Request failed with status ${response.status}.`;
}


// Send a request and handle unsuccessful responses.
async function requestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (!response.ok) {
        throw new Error(await getErrorMessage(response));
    }

    return response.json();
}


// Create a table cell safely.
function createCell(value) {
    const cell = document.createElement("td");
    cell.textContent = value ?? "";
    return cell;
}


// Display tickets in the table.
function renderTickets(tickets) {
    ticketTableBody.replaceChildren();

    if (tickets.length === 0) {
        const row = document.createElement("tr");
        const cell = createCell("No tickets found.");
        cell.colSpan = 7;
        row.appendChild(cell);
        ticketTableBody.appendChild(row);
        return;
    }

    for (const ticket of tickets) {
        const row = document.createElement("tr");

        const createdDate = new Date(ticket.created_at);
        const formattedDate = Number.isNaN(createdDate.getTime())
            ? ticket.created_at
            : createdDate.toLocaleString();

        row.appendChild(createCell(ticket.id));
        row.appendChild(createCell(ticket.title));
        row.appendChild(createCell(ticket.category));
        row.appendChild(createCell(ticket.priority));
        row.appendChild(createCell(ticket.status));
        row.appendChild(createCell(formattedDate));

        const actionCell = document.createElement("td");
        const updateButton = document.createElement("button");

        updateButton.type = "button";
        updateButton.textContent = "Update";

        updateButton.addEventListener("click", () => {
            openUpdateForm(ticket);
        });

        actionCell.appendChild(updateButton);
        row.appendChild(actionCell);

        ticketTableBody.appendChild(row);
    }
}


// Load tickets using the selected status and priority filters.
async function loadTickets() {
    showMessage(listMessage, "Loading tickets...");

    const params = new URLSearchParams();

    const statusValue = document.getElementById("status-filter").value;
    const priorityValue = document.getElementById("priority-filter").value;

    if (statusValue) {
        params.set("status", statusValue);
    }

    if (priorityValue) {
        params.set("priority", priorityValue);
    }

    const queryString = params.toString();
    const url = queryString ? `/tickets?${queryString}` : "/tickets";

    try {
        const tickets = await requestJson(url);

        renderTickets(tickets);
        showMessage(
            listMessage,
            `${tickets.length} ticket(s) found.`
        );
    } catch (error) {
        ticketTableBody.replaceChildren();
        showMessage(
            listMessage,
            `Could not load tickets: ${error.message}`,
            true
        );
    }
}


// Create a ticket through the FastAPI backend.
ticketForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(ticketForm);

    const ticketData = {
        title: formData.get("title").trim(),
        description: formData.get("description").trim(),
        category: formData.get("category").trim(),
        priority: formData.get("priority"),
    };

    showMessage(formMessage, "Creating ticket...");

    try {
        const ticket = await requestJson("/tickets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(ticketData),
        });

        ticketForm.reset();
        filterForm.reset();

        showMessage(
            formMessage,
            `Ticket #${ticket.id} created successfully.`
        );

        await loadTickets();
    } catch (error) {
        showMessage(
            formMessage,
            `Could not create ticket: ${error.message}`,
            true
        );
    }
});


// Apply the selected filters.
filterForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await loadTickets();
});


// Refresh the current ticket list.
document.getElementById("refresh-tickets").addEventListener("click", () => {
    loadTickets();
});


// Clear filters and show all tickets.
document.getElementById("clear-filters").addEventListener("click", () => {
    filterForm.reset();
    loadTickets();
});


// Show the update form for the selected ticket.
function openUpdateForm(ticket) {
    selectedTicketId = ticket.id;

    document.getElementById("selected-ticket-label").textContent =
        `Ticket #${ticket.id}: ${ticket.title}`;

    document.getElementById("update-status").value = ticket.status;
    document.getElementById("update-priority").value = ticket.priority;

    showMessage(updateMessage, "");
    ticketDetails.hidden = false;
    ticketDetails.scrollIntoView({ behavior: "smooth", block: "start" });
}


// Save status and priority changes through FastAPI.
updateTicketForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (selectedTicketId === null) {
        showMessage(updateMessage, "Select a ticket first.", true);
        return;
    }

    const updateData = {
        status: document.getElementById("update-status").value,
        priority: document.getElementById("update-priority").value,
    };

    showMessage(updateMessage, "Saving changes...");

    try {
        const ticket = await requestJson(
            `/tickets/${selectedTicketId}`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(updateData),
            }
        );

        showMessage(
            updateMessage,
            `Ticket #${ticket.id} updated successfully.`
        );

        await loadTickets();
    } catch (error) {
        showMessage(
            updateMessage,
            `Could not update ticket: ${error.message}`,
            true
        );
    }
});


// Close the update form.
document.getElementById("close-details").addEventListener("click", () => {
    ticketDetails.hidden = true;
    selectedTicketId = null;
});


// Load tickets when the JavaScript file is executed.
loadTickets();