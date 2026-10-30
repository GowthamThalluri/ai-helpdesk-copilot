# AI Helpdesk Copilot

A web-based IT support application designed to help support teams create, manage, investigate, and resolve support tickets.

This project demonstrates a practical, end-to-end DevOps journey by progressively implementing application development, containerization, automated testing, Continuous Integration, cloud infrastructure, security, deployment, orchestration, and observability.

## 1. Project Status

**Completed:** Application development, PostgreSQL integration, Docker, Docker Compose, Continuous Integration, and security scanning.

**Current activity:** Finalizing repository documentation and setup instructions.

**Next technical phase:** AWS fundamentals and infrastructure architecture, followed by Terraform.

**Continuous Delivery/Deployment (CD):** Not yet implemented.

The current GitHub Actions workflow builds and scans the Docker image but does not publish it to a container registry or deploy the application to AWS.

## 2. Application Features

The current application provides the following functionality:

- Web-based support ticket dashboard.
- Create new support tickets.
- View existing tickets.
- Filter tickets by status and priority.
- Update ticket status and priority.
- Persistent PostgreSQL database integration.
- Backend health-check endpoint.
- Input validation and error handling.
- Application logging.
- Automated API testing.

### Ticket Statuses

- Open
- In Progress
- Resolved

### Ticket Priorities

- Low
- Medium
- High

AI-assisted ticket classification, summarization, and knowledge assistance are planned for a later development stage.

## 3. Technology Stack

| Area | Technology | Status |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | Implemented |
| Backend | Python, FastAPI | Implemented |
| Database | PostgreSQL | Implemented |
| Database Integration | SQLAlchemy, Psycopg | Implemented |
| Testing | Pytest | Implemented |
| Version Control | Git, GitHub | Implemented |
| Containerization | Docker | Implemented |
| Container Orchestration | Docker Compose | Implemented |
| Continuous Integration | GitHub Actions | Implemented |
| Dependency Security | pip-audit | Implemented |
| Secret Scanning | Gitleaks | Implemented |
| Python Code Security | Bandit | Implemented |
| Container Security | Trivy | Implemented |
| Cloud Infrastructure | AWS | Planned |
| Container Registry | Amazon ECR | Planned |
| Infrastructure as Code | Terraform | Planned |
| Configuration Management | Ansible | Planned |
| Container Orchestration | Kubernetes | Planned |
| Kubernetes Package Management | Helm | Planned |
| Monitoring and Logging | Amazon CloudWatch and other appropriate tools | Planned |

## 4. Application Architecture

The application currently consists of three main components.

1. **Frontend:** HTML, CSS, and JavaScript provide the browser-based user interface.
2. **Backend:** FastAPI processes application requests and implements ticket-management functionality.
3. **Database:** PostgreSQL stores ticket information persistently.

FastAPI serves the frontend and handles application API requests. Docker Compose runs the FastAPI application and PostgreSQL as separate services connected through a Docker network.

### Current Architecture

```text
                 User Browser
                      |
                      v
                Frontend UI
             HTML / CSS / JS
                      |
                      v
               FastAPI Backend
                Python / API
                      |
                      v
                 PostgreSQL
                   Database
```

### Container Architecture

```text
              Docker Compose
                     |
          +----------+----------+
          |                     |
          v                     v
    Application             Database
     Container              Container
          |                     |
       FastAPI              PostgreSQL
          |                     |
          +----------+----------+
                     |
               Docker Network
                     |
                     v
              Persistent Volume
              ai_helpdesk_pgdata
```

## 5. Run the Application Locally

### Prerequisites

- Git
- Docker Desktop
- Docker Compose
- Python 3.13 (for local development and testing)

### Step 1: Clone the repository

```bash
git clone https://github.com/GowthamThalluri/ai-helpdesk-copilot.git

cd ai-helpdesk-copilot
```

### Step 2: Configure environment variables

Create a local environment file from the example:

```bash
cp .env.example .env
```

Open `.env` and configure the database values for your local environment.

The example file contains placeholder values. Replace the placeholder password with your own local development password.

Never commit `.env` or production credentials to GitHub.

### Step 3: Create the persistent Docker volume

The Compose configuration uses an external named Docker volume.

Create it before starting the application:

```bash
docker volume create ai_helpdesk_pgdata
```

This volume stores PostgreSQL data independently of the database container.

### Step 4: Build and start the application

```bash
docker compose up -d --build
```

Docker Compose builds the FastAPI application image and starts the application and PostgreSQL services.

### Step 5: Verify the containers

```bash
docker compose ps
```

Both application and PostgreSQL services should be running. PostgreSQL should report a healthy status.

### Step 6: Open the application

**Frontend:**

http://127.0.0.1:8000/

**Backend health endpoint:**

http://127.0.0.1:8000/health

Expected health response:

```json
{
  "status": "healthy"
}
```

### Step 7: Stop the application

```bash
docker compose down
```

This stops and removes the Compose containers and network.

The external PostgreSQL volume is retained, so ticket data is preserved.

Do not remove the volume using:

```bash
docker volume rm ai_helpdesk_pgdata
```

unless you intentionally want to delete the stored database data.

## 6. Automated Testing

The project uses Pytest for automated API testing.

### Install development dependencies

Make sure the required local environment variables are configured, then install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

### Execute the tests

```bash
python -m pytest -v
```

The current test suite contains 15 tests covering:

- Application health.
- Ticket creation.
- Ticket listing and retrieval.
- Filtering by status and priority.
- Ticket updates.
- Missing-ticket responses.
- Invalid input and validation errors.
- Whitespace-only input validation.

The tests use an isolated in-memory SQLite database so that test execution does not modify the actual PostgreSQL database.

**Latest verified local test result: 15 passed.**

## 7. Continuous Integration and Security

GitHub Actions automates application testing, dependency auditing, source-code security checks, secret scanning, Docker image building, and container vulnerability scanning.

The workflow is located at:

`.github/workflows/tests.yaml`

### Workflow Triggers

The workflow runs when:

- Code is pushed to the `main` branch.
- A pull request targets the `main` branch.

### CI Pipeline Jobs

The workflow contains five jobs.

**Job 1 — Automated Testing**

Tool: Pytest

- Sets up Python 3.13.
- Installs development dependencies.
- Executes the automated application tests.

**Job 2 — Dependency Audit**

Tool: pip-audit

- Checks Python dependencies for known vulnerabilities.
- Audits dependencies listed in `requirements-dev.txt`.

**Job 3 — Repository Secret Scanning**

Tool: Gitleaks

- Scans repository history for accidentally committed secrets.
- Uses full Git history during checkout.

**Job 4 — Python Code Security**

Tool: Bandit

- Scans the Python backend for common security issues.

**Job 5 — Docker Image Build and Security Scanning**

Tools: Docker Buildx and Trivy

- Builds the Docker image using the repository Dockerfile.
- Tags the image as `ai-helpdesk-copilot:ci`.
- Loads the image into the GitHub Actions runner.
- Scans operating-system and application-library vulnerabilities.
- Generates a JSON vulnerability report.
- Uploads the report as a GitHub Actions artifact.
- Runs a separate security gate for fixable HIGH and CRITICAL findings.

The current workflow builds the image but does not publish it to an external container registry.

### Security Gate Policy

The complete Trivy scan includes both fixable and unfixed HIGH and CRITICAL findings.

The separate blocking security gate uses the following policy:

- Fixable HIGH and CRITICAL findings can fail the workflow.
- Findings Trivy classifies as unfixed do not block that particular gate.
- Unfixed findings remain visible in the complete JSON report.

A successful security gate does not mean the Docker image is free from all known vulnerabilities.

For implementation details, see [CI/CD Pipeline Documentation](docs/ci-cd.md).

## 8. Container Security Findings

Trivy is used to scan the application Docker image for known vulnerabilities.

During the latest recorded local scan after runtime image hardening, the findings were:

| Finding | Result |
|---|---:|
| HIGH Debian package vulnerability entries | 44 |
| CRITICAL Debian findings | 0 |
| Python package findings | 0 |

The 44 Debian entries contain repeated package/CVE combinations and do not represent 44 unique vulnerabilities.

During investigation:

- Python findings were traced to components listed in pip's embedded SBOM.
- Pip was removed from the final runtime image after installing application dependencies.
- The application dependencies were verified to remain available.
- A subsequent scan no longer reported Python package findings.
- Debian package versions were checked against the configured Debian 13 (Trixie) repositories.
- No newer candidate versions were available for the checked packages during that investigation.

The Debian findings remain unresolved and tracked. They are not treated as fixed simply because the CI security gate passed.

For the detailed investigation, see [Container Security Scan Documentation](docs/security-scan.md).

## 9. Project Documentation

| Document | Description |
|---|---|
| [Project Requirements](docs/requirements.md) | Initial application requirements and scope |
| [Project Progress](docs/progress.md) | Completed work, current status, and roadmap |
| [CI/CD Pipeline](docs/ci-cd.md) | GitHub Actions workflow and CI implementation |
| [Security Scan](docs/security-scan.md) | Trivy findings and security decisions |

## 10. Project Roadmap

The project follows a progressive implementation approach. Each milestone must be implemented, tested, documented, and verified before moving to the next.

### Phase 0 — Repository Documentation and Setup

- [x] Create initial project requirements.
- [x] Implement the application and database integration.
- [x] Implement automated application tests.
- [x] Implement Docker and Docker Compose.
- [x] Implement Continuous Integration.
- [x] Implement security scanning.
- [x] Document container security findings.
- [ ] Complete repository documentation synchronization.
- [ ] Verify a fresh-clone setup using the documented instructions.
- [ ] Commit and push the documentation updates.

### Phase 1 — AWS Fundamentals and Infrastructure Architecture

- [ ] Review IAM and least-privilege access.
- [ ] Understand AWS Regions and Availability Zones.
- [ ] Understand VPC architecture.
- [ ] Learn public and private subnets.
- [ ] Understand route tables, Internet Gateways, and NAT.
- [ ] Learn security groups and network access.
- [ ] Evaluate EC2 and appropriate application hosting choices.
- [ ] Understand Amazon ECR for container image storage.
- [ ] Review CloudWatch and secrets management.
- [ ] Plan infrastructure costs, security, and resource cleanup.

### Phase 2 — Terraform and Infrastructure as Code

- [ ] Understand Infrastructure as Code.
- [ ] Learn Terraform providers and resources.
- [ ] Learn variables, outputs, and data sources.
- [ ] Understand Terraform state and state management.
- [ ] Practise `terraform init`.
- [ ] Practise `terraform fmt`.
- [ ] Practise `terraform validate`.
- [ ] Understand `terraform plan`.
- [ ] Practise `terraform apply`.
- [ ] Practise safe resource cleanup using `terraform destroy`.
- [ ] Organize reusable Terraform configurations.
- [ ] Provision the required AWS infrastructure for the project.

### Phase 3 — Ansible and Configuration Management

- [ ] Understand configuration management.
- [ ] Learn Ansible inventory.
- [ ] Practise ad-hoc commands.
- [ ] Learn playbooks.
- [ ] Learn variables and handlers.
- [ ] Learn roles.
- [ ] Automate required host-configuration tasks.
- [ ] Integrate Ansible where appropriate for the selected architecture.

### Phase 4 — Complete Continuous Delivery/Deployment

- [ ] Publish verified Docker