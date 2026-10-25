# AI Helpdesk Copilot — Requirements

## 1. Project Purpose

Build a web application that helps IT support teams create,
track, investigate, and resolve support tickets.

## 2. Initial Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python and FastAPI
- Database: PostgreSQL
- Version control: Git and GitHub

## 3. Version 1 Features

1. Display a ticket dashboard.
2. Create a ticket with a title, description, category, and priority.
3. List and view saved tickets.
4. Filter tickets by status and priority.
5. Update a ticket's status and priority.
6. Persist ticket data in PostgreSQL.
7. Provide a backend health-check endpoint.

## 4. Ticket Statuses

- Open
- In Progress
- Resolved

## 5. Ticket Priorities

- Low
- Medium
- High

## 6. Operational Requirements

- Validate incoming requests.
- Handle errors clearly.
- Read application configuration from environment variables.
- Never commit passwords, tokens, or API keys to GitHub.
- Add automated tests and useful application logs.
- Verify the application before moving to the next milestone.

## 7. Future Enhancements

- Troubleshooting suggestions and AI-assisted responses.
- Authentication and authorization.
- Docker and automated CI/CD.
- AWS deployment and infrastructure automation.
- Kubernetes deployment.
- Monitoring, logging, and alerting.
- A later refactor into microservices.

## 8. Version 1 Completion Criteria

- A user can create and view tickets through the UI.
- Ticket data remains available after application restarts.
- A user can update ticket status and priority.
- Invalid input is rejected appropriately.
- The health endpoint works.
- Automated tests pass.
EOF