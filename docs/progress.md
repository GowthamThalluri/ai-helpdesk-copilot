
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
- Verified ticket creation, retrieval, filtering, and updates through the API.
- Verified ticket data persists after restarting FastAPI.
- Verified database records directly using PostgreSQL.
- Committed and pushed the backend and database integration to GitHub.

## Frontend Development — Completed

### Completed
- Created the dashboard using HTML and CSS.
- Added JavaScript for ticket creation, listing, filtering, and updates.
- Configured FastAPI to serve the frontend and static assets.
- Verified the dashboard loads on the local machine.
- Tested ticket creation through the UI.
- Tested status, priority, and combined filters.
- Tested ticket status and priority updates through the UI.
- Verified UI changes persist in PostgreSQL.
- Committed and pushed the frontend to GitHub.

## Automated Testing — Completed

### Completed
- Added development dependencies in `requirements-dev.txt`.
- Added automated API tests in `tests/test_tickets.py`.
- Used an isolated in-memory SQLite database so tests do not modify real PostgreSQL data.
- Tested the health endpoint, ticket creation, listing, filtering, retrieval, updates, and error responses.
- Resolved the Starlette test-client deprecation warning by updating the test dependencies.
- Verified all eight tests pass using `python -m pytest -v`.
- Verified dependencies using `python -m pip check`.
- Committed and pushed the testing milestone to GitHub.

## Current Limitations

- Automated tests do not yet cover every validation failure or database error scenario.
- Logging and error handling need further refinement.
- The frontend has been manually tested but does not yet have automated browser tests.
- The FastAPI application has not yet been containerized. PostgreSQL currently runs separately in Docker Desktop.
- CI/CD, security scanning, cloud deployment, and infrastructure automation are still pending.

## Next Milestone — Application Hardening

- Expand automated tests for invalid input and validation failures.
- Improve error handling and application logging.
- Document expected HTTP error responses in the API specification.
- Verify the complete frontend-to-backend-to-database workflow.
- Review the application before containerization.


## When Core DevOps Engineering Starts

The application foundation is built. The next step is application hardening, followed by the main DevOps delivery and operations workflow.

### Core DevOps Milestones

1. **Docker and Docker Compose — First Core DevOps Milestone**
   - Write a Dockerfile for the FastAPI application.
   - Build and run the application container.
   - Configure the application and PostgreSQL using Docker Compose.
   - Handle environment variables, networking, persistent storage, and health checks.
   - Verify that the application works independently of the local Python development setup.

2. **CI/CD with GitHub Actions**
   - Automatically run tests when code is pushed.
   - Add code-quality and security checks.
   - Build and tag Docker images.
   - Automate delivery through a controlled deployment workflow.

3. **Cloud Deployment and Infrastructure as Code**
   - Deploy the application to AWS.
   - Use Terraform to provision infrastructure.
   - Use Ansible where configuration management is appropriate.
   - Apply least-privilege access, secrets management, and cost controls.

4. **Kubernetes and Operations**
   - Deploy the application to Kubernetes.
   - Configure deployments, services, health probes, and resource limits.
   - Add monitoring, logging, alerting, and troubleshooting exercises.
   - Test failure recovery and document what happens.

### Project Readiness Rule

Do not mark a milestone complete merely because configuration files exist. Complete it only after running the relevant commands, testing the result, resolving failures, and documenting the evidence.


## Future DevOps Milestones

1. Complete application validation, error handling, and logging.
2. Containerize the application and database workflow using Docker and Docker Compose.
3. Build CI/CD pipelines using GitHub Actions.
4. Add automated security and code-quality checks.
5. Deploy the application to AWS.
6. Introduce Terraform and Ansible for infrastructure automation and configuration management.
7. Deploy and operate the application on Kubernetes.
8. Implement monitoring, logging, alerting, and failure troubleshooting.
9. Evaluate a microservices architecture after the initial application is stable.

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
- Do not use Ubuntu/WSL for this project unless a requirement justifies it and the approach is reviewed first.
