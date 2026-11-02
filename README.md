# AI Helpdesk Copilot

A web-based IT support application designed to help support teams create, manage, investigate, and resolve support tickets.

This project demonstrates a practical, end-to-end DevOps journey by progressively implementing application development, containerization, automated testing, Continuous Integration, database migrations, cloud infrastructure, security, deployment, orchestration, and observability.

## 1. Project Status

**Completed:** Application development, PostgreSQL integration, Docker, Docker Compose, Alembic database migrations, automated testing, Continuous Integration, and security scanning.

**Current activity:** Finalizing repository documentation and completing the final fresh-clone deployment verification.

**Next technical phase:** AWS fundamentals and infrastructure architecture, followed by Terraform.

**Continuous Delivery/Deployment (CD):** Not yet implemented.

The current GitHub Actions workflow builds and scans the Docker image but does not publish it to a container registry or deploy the application to AWS.

## 2. Application Features

The current application provides:

- Web-based IT support dashboard.
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

## 3. Technology Stack

| Area | Technology | Status |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | Implemented |
| Backend | Python, FastAPI | Implemented |
| Database | PostgreSQL | Implemented |
| Database Integration | SQLAlchemy, Psycopg | Implemented |
| Database Migrations | Alembic | Implemented |
| Version Control | Git, GitHub | Implemented |
| Containers | Docker | Implemented |
| Container Orchestration | Docker Compose | Implemented |
| Automated Testing | Pytest, HTTPX | Implemented |
| Continuous Integration | GitHub Actions | Implemented |
| Dependency Scanning | pip-audit | Implemented |
| Source Code Scanning | Bandit | Implemented |
| Secret Scanning | Gitleaks | Implemented |
| Container Scanning | Trivy | Implemented |
| Cloud | AWS | Planned |
| Container Registry | Amazon ECR | Planned |
| Infrastructure as Code | Terraform | Planned |
| Configuration Management | Ansible | Planned |
| Orchestration | Kubernetes | Planned |
| Package Management | Helm | Planned |
| Monitoring and Logging | CloudWatch and appropriate observability tools | Planned |

## 4. Application Architecture

The application currently contains three main components:

1. **Frontend:** Provides the browser-based user interface.
2. **Backend:** FastAPI processes requests and implements application logic.
3. **Database:** PostgreSQL stores ticket information persistently.

SQLAlchemy manages database communication. Alembic manages database schema changes through version-controlled migration scripts.

### Current Docker Compose Architecture

```text
                  User / Browser
                        |
                        |
                 127.0.0.1:8000
                        |
                        v
               +------------------+
               |   FastAPI App    |
               |   (Non-root)     |
               +------------------+
                        |
                        |
                  Docker Network
                        |
                        v
               +------------------+
               |    PostgreSQL    |
               |                  |
               |   Persistent     |
               |     Volume       |
               +------------------+


             Database Startup Flow
             ---------------------

               PostgreSQL starts
                       |
                       v
               Health check passes
                       |
                       v
               Alembic migration
                   service
                       |
                       v
               Migration succeeds
                       |
                       v
                 FastAPI starts
```

The migration service runs once during deployment. FastAPI starts only after the migration service completes successfully.

## 5. Database Schema and Migrations

The project uses PostgreSQL for persistent ticket storage and Alembic for database schema versioning.

### Why Alembic?

Without database migrations, a newly initialized PostgreSQL database may not contain the tables required by the application.

Alembic provides a controlled way to:

- Create database tables.
- Modify existing database schemas.
- Track database schema versions.
- Apply pending changes during deployment.
- Roll back supported schema changes.

### Migration History

The current migration history contains two revisions.

| Revision | Description |
|---|---|
| `e91d904ff8b7` | Create the tickets table and historical index |
| `f1b9ab28aaf3` | Remove the redundant tickets ID index |

The initial revision represents the original database schema. The second revision removes the unnecessary secondary index on the primary-key column.

The PostgreSQL primary-key index remains in place.

### Automatic Migration During Deployment

The Docker Compose configuration contains three services:

| Service | Responsibility |
|---|---|
| `postgres` | Runs PostgreSQL and stores ticket data |
| `migrate` | Applies pending Alembic migrations |
| `app` | Runs the FastAPI application |

The migration service executes:

```bash
alembic upgrade head
```

The FastAPI service depends on the migration service completing successfully.

This ensures that the application does not start against an outdated or uninitialized database schema.

### Fresh Database Initialization

For a completely new installation:

1. Configure `.env`.
2. Create the required external Docker volume.
3. Start the application using Docker Compose.

Docker Compose automatically applies both migrations to the empty database before starting FastAPI.

### Existing Database Upgrade

For an existing database created before Alembic was introduced, the initial migration must be baselined before normal deployment.

First, back up the database and verify that the existing schema matches the initial migration.

Build the application image:

```bash
docker compose build app
```

Record the existing schema as Revision 1:

```bash
docker compose run --rm migrate alembic stamp e91d904ff8b7
```

This records the migration revision without executing the initial table-creation operation.

Then start the application:

```bash
docker compose up -d --build
```

The migration service applies any remaining migrations automatically.

**Important:** Do not run the baseline command against a fresh database. Do not blindly baseline an existing database without checking its actual schema and taking a backup.

## 6. Local Development Setup

### Prerequisites

- Git
- Docker Desktop
- Docker Compose
- Python 3.13 (for local development and testing)
- VS Code or another code editor

### Step 1: Clone the repository

```bash
git clone https://github.com/GowthamThalluri/ai-helpdesk-copilot.git

cd ai-helpdesk-copilot
```

### Step 2: Configure environment variables

Create a local environment file:

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

Docker Compose builds the application image and starts the services in the required order:

1. PostgreSQL starts.
2. PostgreSQL passes its health check.
3. Alembic applies pending migrations.
4. FastAPI starts after successful migration completion.

### Step 5: Verify the containers

```bash
docker compose ps -a
```

Expected service states:

- PostgreSQL: `Up (healthy)`
- Migration: `Exited (0)`
- FastAPI: `Up`

The migration container exits after completing its one-time task. Exit code `0` means the migration completed successfully.

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

**Ticket API:**

http://127.0.0.1:8000/tickets

### Step 7: Inspect application logs

```bash
docker compose logs app
```

Inspect migration logs:

```bash
docker compose logs migrate
```

Inspect PostgreSQL logs:

```bash
docker compose logs postgres
```

### Step 8: Stop the application

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

## 7. Automated Testing

The project uses Pytest and HTTPX for automated API testing.

### Install development dependencies

Create and activate the Python virtual environment:

```bash
python -m venv .venv
```

For Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

### Run tests

```bash
python -m pytest -q
```

The tests use an isolated in-memory SQLite database so that test execution does not modify the actual PostgreSQL database.

### Current Test Coverage

The automated tests cover:

- Health endpoint.
- Ticket creation.
- Ticket listing.
- Ticket filtering.
- Single-ticket retrieval.
- Ticket updates.
- Missing-ticket responses.
- Invalid priorities.
- Invalid status filters.
- Missing required fields.
- Invalid titles and whitespace-only inputs.
- Validation and error responses.

**Latest verified result:** 15 tests passed.

## 8. Continuous Integration and Security

The project uses GitHub Actions for automated quality checks and Docker image scanning.

### Current CI Jobs

| Job | Purpose |
|---|---|
| Test | Executes automated application tests |
| Dependency Audit | Checks dependencies using pip-audit |
| Secret Scan | Scans repository history using Gitleaks |
| Bandit Scan | Checks Python code for security issues |
| Build Image | Builds and scans the Docker image |

The Docker image build waits for the preceding quality and security jobs to complete successfully.

### Container Security

The Dockerfile includes:

- Python slim base image.
- Non-root application user.
- Dependency installation during image build.
- Removal of pip from the final runtime image.
- Minimal application files copied into the container.

Trivy scans the built image for vulnerabilities.

The project documents unresolved container operating-system package findings and the CI gate policy.

A successful CI run does not mean that every reported vulnerability is absent. Review `docs/security-scan.md` for the current findings and decisions.

### CI/CD Documentation

See:

[CI/CD Pipeline Documentation](docs/ci-cd.md)

### Security Documentation

See:

[Container Security Scan Documentation](docs/security-scan.md)

**Continuous Delivery/Deployment is not yet implemented.** The current workflow does not push the image to Amazon ECR or deploy the application to AWS.

## 9. Project Documentation

| Document | Description |
|---|---|
| [Project Requirements](docs/requirements.md) | Initial application requirements and scope |
| [Project Progress](docs/progress.md) | Completed work, current status, and roadmap |
| [CI/CD Pipeline](docs/ci-cd.md) | GitHub Actions workflow and CI implementation |
| [Security Scan](docs/security-scan.md) | Trivy findings and security decisions |

## 10. Project Roadmap

The project follows a progressive implementation approach. Each milestone must be implemented, tested, documented, and verified before moving to the next.

### Phase 0 — Application, Docker, CI, Security, and Repository Setup

- [x] Create initial project requirements.
- [x] Implement the application and PostgreSQL integration.
- [x] Implement automated application tests.
- [x] Implement Docker and Docker Compose.
- [x] Implement Continuous Integration.
- [x] Implement dependency, secret, source-code, and container security scanning.
- [x] Document container security findings.
- [x] Implement version-controlled database migrations using Alembic.
- [x] Integrate automatic migrations into Docker Compose startup.
- [x] Safely baseline the existing PostgreSQL database.
- [x] Preserve all five existing tickets during migration.
- [x] Verify the original application after migration.
- [ ] Verify a fresh-clone setup using the final two-revision migration history.
- [ ] Complete repository documentation synchronization.
- [ ] Commit and push the final implementation.
- [ ] Verify GitHub Actions after the final changes.

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
- [ ] Learn Ansible inventory and configuration.
- [ ] Learn playbooks, tasks, and modules.
- [ ] Understand variables, handlers, and templates.
- [ ] Learn Ansible roles.
- [ ] Practise configuration management where required by the project.

### Phase 4 — Continuous Delivery and AWS Deployment

- [ ] Understand the difference between CI and CD.
- [ ] Publish verified images to Amazon ECR.
- [ ] Configure secure GitHub Actions authentication with AWS.
- [ ] Use appropriate AWS IAM roles and permissions.
- [ ] Deploy the application to the selected AWS runtime.
- [ ] Automate deployment through GitHub Actions.
- [ ] Add deployment health verification.
- [ ] Practise rollout and rollback procedures.

### Phase 5 — Kubernetes

- [ ] Learn Kubernetes architecture.
- [ ] Understand Pods and Deployments.
- [ ] Learn Services and service discovery.
- [ ] Understand ConfigMaps and Secrets.
- [ ] Learn readiness and liveness probes.
- [ ] Understand resource requests and limits.
- [ ] Practise autoscaling.
- [ ] Deploy the application locally using Minikube.
- [ ] Evaluate Amazon EKS for cloud deployment.

### Phase 6 — Helm

- [ ] Understand Helm charts and their structure.
- [ ] Learn chart templates and values files.
- [ ] Create a Helm chart for the application.
- [ ] Configure environment-specific values.
- [ ] Practise Helm install, upgrade, rollback, and uninstall.

### Phase 7 — Monitoring, Logging, and Observability

- [ ] Understand monitoring and observability fundamentals.
- [ ] Implement infrastructure and application metrics.
- [ ] Centralize application logs.
- [ ] Configure dashboards and alerting.
- [ ] Monitor application and database health.
- [ ] Practise troubleshooting from logs and metrics.

### Phase 8 — Reliability and Failure Testing

- [ ] Introduce controlled application failures.
- [ ] Test database unavailability.
- [ ] Test container restart and recovery.
- [ ] Verify persistent data after failures.
- [ ] Practise backup and restore procedures.
- [ ] Document troubleshooting and recovery procedures.

### Phase 9 — AI Capabilities and Architecture Evolution

- [ ] Evaluate AI-assisted ticket summarization.
- [ ] Explore ticket classification.
- [ ] Add knowledge-base assistance.
- [ ] Evaluate AI-generated troubleshooting suggestions.
- [ ] Measure the usefulness and reliability of AI features.
- [ ] Evaluate microservices only when justified by application requirements.

---

## Learning Approach

This project follows a hands-on approach:

1. Understand the requirement.
2. Understand the underlying concept.
3. Implement the solution.
4. Test the result.
5. Troubleshoot failures.
6. Document the outcome.
7. Verify completion before proceeding.

Features and milestones will be marked complete only after they have been implemented and verified.