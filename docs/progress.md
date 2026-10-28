
# AI Helpdesk Copilot — Project Progress

## Day 1 — Project Foundations

### Completed
- Verified the GitHub repository and `main` branch.
- Verified the Windows development environment using Git Bash, Python, and Docker Desktop.
- Defined the initial application requirements and Version 1 scope.
- Selected HTML, CSS, and JavaScript for the frontend, FastAPI for the backend, and PostgreSQL for the database.
- Created the project README and requirements documentation.
- Added `.gitignore` and `.gitattributes`.
- Published the project foundation and configuration changes to GitHub.

## Day 2 — Backend and Database Foundation

### Completed
- Created the Python virtual environment `.venv` on Windows.
- Installed FastAPI, Uvicorn, SQLAlchemy, Psycopg, and python-dotenv.
- Implemented the FastAPI application and health endpoint.
- Created ticket validation and response schemas.
- Implemented ticket creation, listing, filtering, single-ticket retrieval, and status/priority updates.
- Added handling for nonexistent tickets and empty update requests.
- Configured PostgreSQL using Docker Desktop and a persistent named volume.
- Created the SQLAlchemy database model and PostgreSQL connection/session management.
- Connected the ticket API to PostgreSQL.
- Verified ticket creation, retrieval, filtering, and updates through the API documentation.
- Verified that ticket data persists after restarting FastAPI.
- Verified database records directly using PostgreSQL.
- Committed and pushed the backend and database integration to GitHub.

## Frontend Development — Completed

### Completed
- Created the dashboard using HTML and CSS.
- Added JavaScript for ticket creation, listing, filtering, and updates.
- Configured FastAPI to serve the frontend and static assets.
- Verified that the dashboard loads locally through FastAPI.
- Tested ticket creation through the UI.
- Tested status filtering, priority filtering, and combined filtering.
- Tested ticket status and priority updates through the UI.
- Verified that UI updates persist in PostgreSQL.
- Committed and pushed the frontend to GitHub.

## Automated Testing — Completed

### Completed
- Created `requirements-dev.txt` for development and testing dependencies.
- Added automated API tests in `tests/test_tickets.py`.
- Used an isolated in-memory SQLite database so tests do not modify real PostgreSQL data.
- Tested the health endpoint, ticket creation, listing, filtering, retrieval, updates, and error responses.
- Tested invalid priorities, short titles, missing required fields, and invalid status filters.
- Added tests for whitespace-only titles, descriptions, and categories.
- Resolved the Starlette test-client deprecation warning by updating the test dependencies.
- Verified that all 15 automated tests pass using `python -m pytest -v`.
- Verified dependencies using `python -m pip check`.
- Committed and pushed the automated testing milestone to GitHub.

## Application Hardening — Verified Locally

### Completed
- Added whitespace trimming and validation for ticket creation inputs.
- Expanded automated tests for invalid requests and validation failures.
- Documented `400 Bad Request` and `404 Not Found` responses in the FastAPI OpenAPI specification.
- Added application logging using Python's built-in logging library.
- Added informational logs for ticket creation and updates.
- Added warning logs when a requested ticket is not found.
- Verified that missing-ticket warnings appear in the running application's terminal.
- Verified Python syntax and confirmed all 15 automated tests pass after the hardening changes.

### Publication Status
- Application hardening changes have been verified locally.
- The latest hardening changes and progress documentation still need to be committed and pushed to GitHub.

## Current Limitations

- Database failure and transaction-rollback scenarios need additional testing.
- The frontend has been tested manually but does not yet have automated browser tests.
- The FastAPI application has not yet been containerized.
- PostgreSQL currently runs separately in Docker Desktop; the application is not yet running in its own container.
- CI/CD, automated security scanning, cloud deployment, and infrastructure automation remain pending.
- Database schema migrations have not yet been configured.

## When Core DevOps Engineering Starts

The application foundation is built. After the current hardening changes are committed and pushed, the project will move into its first core DevOps milestone.

### First Core DevOps Milestone — Docker and Docker Compose

- Write a Dockerfile for the FastAPI application.
- Build the application Docker image.
- Run the FastAPI application inside a container.
- Use Docker Compose to run the application and PostgreSQL together.
- Configure environment variables and keep credentials out of source control.
- Configure container networking and persistent database storage.
- Add health checks and verify service readiness.
- Inspect container logs and troubleshoot startup and connectivity failures.
- Verify that the application works without relying on the local Python development server.
- Run automated tests to confirm the application still works after containerization.

### How This Milestone Will Be Verified

Do not mark containerization complete merely because the Dockerfile or Compose file exists. Completion requires:
- Successfully building the image.
- Successfully starting the services.
- Creating and retrieving tickets through the running application.
- Verifying database persistence.
- Testing health checks and troubleshooting at least one failure scenario.
- Documenting the commands used and the observed results.

## Future DevOps Milestones

1. **Docker and Docker Compose:** Package and run the application with its database.

## Docker and Docker Compose — Completed Locally

### Docker fundamentals and practical work
- Learned Docker images, containers, the Docker client, daemon, registries, networks, port publishing, and persistent volumes.
- Inspected existing Docker images, containers, networks, logs, and container configuration.
- Diagnosed and recovered the existing PostgreSQL container without deleting its database volume.
- Verified that all five ticket records remained available after container recovery.

### Application containerization
- Renamed the backend directory from `app/` to `backend/`.
- Updated Python imports, the Dockerfile, and the Uvicorn startup module.
- Created `.dockerignore` to exclude local secrets, virtual environments, test artifacts, Git metadata, and unnecessary documentation.
- Created a Dockerfile using `python:3.13-slim`.
- Built the application image `ai-helpdesk-copilot:1.0`, then rebuilt `ai-helpdesk-copilot:1.1` after the backend directory rename.
- Ran FastAPI in the `ai-helpdesk-app` container.
- Configured the database hostname and port through environment variables.
- Published FastAPI on `127.0.0.1:8000`.

### Docker networking and persistence
- Created the custom network `ai-helpdesk-network`.
- Connected the existing PostgreSQL container using the network alias `postgres`.
- Reused the named volume `ai_helpdesk_pgdata`.
- Verified that FastAPI could communicate with PostgreSQL through the Docker network.

### Docker Compose
- Created `compose.yaml` to define the FastAPI and PostgreSQL services.
- Configured the application build, environment variables, published ports, persistent storage, PostgreSQL health check, service dependency, and restart policies.
- Reused the existing external PostgreSQL volume to preserve database records.
- Migrated from manually managed containers to Compose-managed services.
- Verified that `docker compose config --quiet` succeeds.
- Verified that both services start successfully and PostgreSQL becomes healthy.
- Confirmed that `/health` returns HTTP 200.
- Confirmed that `GET /tickets` returns all five tickets.
- Verified that the dashboard displays all five tickets after the Compose migration.
- Confirmed that all 15 automated tests pass locally.

### Status
- Dockerfile, image build, application container, networking, and basic Docker Compose setup are verified locally.
- Changes still need to be committed and pushed to GitHub.
- CI/CD, container security scanning, cloud deployment, and infrastructure automation remain pending.

2. **CI/CD with GitHub Actions:** Automatically run tests, quality checks, security checks, and image builds when code changes.
3. **Security and code quality:** Add appropriate dependency, source-code, and container image scanning.
4. **AWS deployment:** Deploy the application using an appropriate cloud architecture, with cost and access controls.
5. **Infrastructure as Code:** Use Terraform to provision infrastructure and Ansible where configuration management is appropriate.
6. **Kubernetes:** Deploy and operate the application with deployments, services, health probes, and resource limits.
7. **Monitoring and observability:** Implement metrics, logging, alerting, and troubleshooting.
8. **Failure testing:** Practise diagnosing failures, recovering services, and verifying persistence.
9. **Architecture evolution:** Evaluate a microservices architecture only after the initial application is stable.

## Working Rule

For every milestone:
1. Understand the requirement.
2. Implement the task.
3. Test the result.
4. Troubleshoot failures.
5. Document the outcome.
6. Verify completion before proceeding.

## Development Environment Rule

- Use VS Code for editing.
- Use Windows Git Bash for Git and development commands.
- Use the Windows Python virtual environment for Python development.
- Use Docker Desktop for containers and the local PostgreSQL database.
- Keep `.env` and all credentials out of Git.
- Do not use Ubuntu/WSL for this project unless a requirement justifies it and the approach is reviewed first.
