# AI Helpdesk Copilot

A web-based IT support application designed to help support teams create, manage, investigate, and resolve support tickets.

This project demonstrates a practical, end-to-end DevOps journey by progressively implementing application development, containerization, automated testing, Continuous Integration, database migrations, security, Kubernetes orchestration, GitOps, and observability. The main portfolio implementation is being completed locally. Real AWS deployment is a later optional extension.

## 1. Project Status

**Completed:** Application development, PostgreSQL integration, Docker, Docker Compose, Alembic database migrations, 17 automated tests, GitHub Actions Continuous Integration, dependency/source-code/secret/container security scanning, database readiness checks, database outage and recovery verification, and PostgreSQL backup and restore verification.

**Current implementation environment:** Windows Git Bash, VS Code, Docker Desktop, and the existing local Minikube installation.

**Current activity:** Preparing to deploy the existing FastAPI and PostgreSQL application to local Kubernetes using Minikube.

**Next technical phase:** Kubernetes deployment with Minikube, followed by Helm, local Infrastructure as Code practice, Ansible, GitOps with Argo CD, and monitoring with Prometheus and Grafana.

**Continuous Integration:** Implemented using GitHub Actions. The workflow tests the application, audits dependencies, scans for secrets, runs Bandit, builds the Docker image, and scans the image with Trivy.

**Continuous Delivery/Deployment:** Not yet implemented. The current GitHub Actions workflow does not publish the image to a registry or deploy the application.

**Cloud deployment:** Not part of the current local project milestone. Existing AWS/Terraform work is preserved as project history. A real AWS deployment can be considered after the local portfolio version is complete.

## 2. Application Features

The current application provides:

- Web-based IT support dashboard.
- Create new support tickets.
- View existing tickets.
- Filter tickets by status and priority.
- Update ticket status and priority.
- Persistent PostgreSQL database integration.
- Liveness endpoint at `/health` to report whether the FastAPI process is responding.
- Readiness endpoint at `/ready` to check whether the application can communicate with PostgreSQL.
- Input validation and controlled error responses.
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
| Local Container Orchestration | Minikube / Kubernetes | Next phase |
| Package Management | Helm | Planned |
| Infrastructure as Code | Terraform | AWS network foundation committed; local practice planned |
| Configuration Management | Ansible | Planned |
| GitOps | Argo CD | Planned |
| Metrics and Dashboards | Prometheus, Grafana | Planned |
| Cloud | AWS | Later optional extension |
| Container Registry | Amazon ECR | Later optional extension |

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
                       v
                127.0.0.1:8000
                       |
                       v
              +------------------+
              |   FastAPI App    |
              |    Non-root      |
              +------------------+
                       |
                       | Docker Network
                       v
              +------------------+
              |    PostgreSQL    |
              |                  |
              | Persistent Volume|
              +------------------+

             Database Startup Flow
             ----------------------

              PostgreSQL starts
                      |
                      v
              Health check passes
                      |
                      v
              Alembic migration service
                      |
                      v
              Migration succeeds
                      |
                      v
                FastAPI starts
```

The Compose migration service runs once during deployment. FastAPI starts only after the migration service completes successfully.

### Health and Readiness Checks

The application exposes two different checks:

- `GET /health` — confirms that the FastAPI application process is responding.
- `GET /ready` — executes a lightweight database query and confirms that PostgreSQL is reachable.

The distinction was verified during a controlled PostgreSQL outage:

| Scenario | `/health` | `/ready` |
|---|---|---|
| PostgreSQL available | HTTP 200 | HTTP 200 |
| PostgreSQL stopped | HTTP 200 | HTTP 503 |
| PostgreSQL restarted and healthy | HTTP 200 | HTTP 200 |

This separation will be used when configuring Kubernetes liveness and readiness probes.

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

The initial revision represents the original database schema. The second revision removes the unnecessary secondary index on the primary-key column. The PostgreSQL primary-key index remains in place.

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

The FastAPI service depends on the migration service completing successfully. This ensures that the application does not start against an outdated or uninitialized database schema.

### Fresh Database Initialization

A fresh, isolated PostgreSQL database was tested on November 12, 2026:

1. Confirmed that the temporary database contained no tables.
2. Ran `alembic upgrade head` using the application image.
3. Verified both migration revisions ran in order.
4. Confirmed `alembic current` reported `f1b9ab28aaf3 (head)`.
5. Inspected the resulting `tickets` table and primary-key index.
6. Started a separate FastAPI container against the migrated database.
7. Verified `/health` and `/tickets` returned HTTP 200.
8. Removed only the temporary test resources.

The original PostgreSQL volume was not used by this test.

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

Open `.env` and configure the database values for your local environment. The example file contains placeholder values. Replace the placeholder password with your own local development password.

Never commit `.env` or production credentials to GitHub.

### Step 3: Create the persistent Docker volume

The Compose configuration uses an external named Docker volume. Create it before starting the application:

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

**Liveness endpoint:**

http://127.0.0.1:8000/health

Expected response:

```json
{"status": "healthy"}
```

**Readiness endpoint:**

http://127.0.0.1:8000/ready

Expected response while PostgreSQL is available:

```json
{"status": "ready", "database": "connected"}
```

**Ticket API:**

http://127.0.0.1:8000/tickets

### Step 7: Inspect application logs

```bash
docker compose logs app
docker compose logs migrate
docker compose logs postgres
```

### Step 8: Stop the application

```bash
docker compose down
```

This stops and removes the Compose containers and network. The external PostgreSQL volume is retained, so ticket data is preserved.

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

- Liveness endpoint.
- Readiness endpoint when the database is available.
- Readiness endpoint returning HTTP 503 for a simulated database failure.
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

**Latest locally verified result:** 17 tests passed.

The tests were executed using:

```bash
python -m pytest -q
```

## 8. Database Reliability Verification

The following DevOps reliability exercises were completed on November 12, 2026.

### Controlled Database Outage and Recovery

- Verified `/health` and `/ready` while PostgreSQL was healthy.
- Stopped only the PostgreSQL Compose service using `docker compose stop postgres`.
- Confirmed FastAPI remained running and `/health` returned HTTP 200.
- Confirmed `/ready` returned HTTP 503 with a controlled database-unavailable response.
- Restarted PostgreSQL using `docker compose start postgres`.
- Waited for the PostgreSQL health check to report `healthy`.
- Confirmed `/ready` returned HTTP 200 after recovery.
- Confirmed all five original tickets remained available.

### PostgreSQL Backup and Restore

- Created a PostgreSQL custom-format backup outside the project repository.
- Confirmed the backup file was non-empty and generated a SHA-256 checksum.
- Inspected the archive with `pg_restore --list`.
- Confirmed the archive contained the `tickets` table, ticket data, `alembic_version`, and the ticket ID sequence.
- Started a separate temporary PostgreSQL container with a separate anonymous Docker volume.
- Restored the backup into the empty temporary database.
- Verified that the restored database contained five tickets.
- Verified the restored Alembic revision was `f1b9ab28aaf3`.
- Removed only the temporary restore container and its anonymous volume.
- Rechecked the original database and confirmed all five original tickets were still present.

**Result:** Backup archive inspection and isolated restore verification passed. The original database volume was not overwritten or deleted.

## 9. Continuous Integration and Security

The project uses GitHub Actions for automated quality checks and Docker image scanning.

### Current CI Jobs

| Job | Purpose |
|---|---|
| Test | Executes automated application tests |
| Dependency Audit | Checks dependencies using pip-audit |
| Secret Scan | Scans repository history using Gitleaks |
| Bandit Scan | Checks Python code for security issues |
| Build Image | Builds and scans the Docker image |

The Docker image build waits for the preceding quality and security jobs to complete successfully. The image is built and scanned but is not pushed to an external registry.

The latest workflow triggered by commit `89567e6` completed successfully, according to the GitHub Actions result verified during this project milestone.

### Container Security

The Dockerfile includes:

- Python slim base image.
- Non-root application user.
- Dependency installation during image build.
- Removal of pip from the final runtime image.
- Minimal application files copied into the container.
- A Debian `zlib1g` package update addressing the two fixable HIGH findings identified by the earlier Trivy scan.

Trivy scans the built image for vulnerabilities. The project documents the findings, fixes, and CI gate policy in `docs/security-scan.md`.

A successful CI run does not mean that every reported vulnerability is absent. Review `docs/security-scan.md` for the recorded findings and decisions.

### CI/CD Documentation

See [CI/CD Pipeline Documentation](docs/ci-cd.md).

[Container Security Scan Documentation](docs/security-scan.md) records Trivy findings and security decisions.

**Continuous Delivery/Deployment is not yet implemented.** The current workflow does not push the image to a container registry or deploy the application.

## 10. Project Documentation

| Document | Description |
|---|---|
| [Project Requirements](docs/requirements.md) | Initial application requirements and scope |
| [Project Progress](docs/progress.md) | Completed work, current status, and roadmap |
| [CI/CD Pipeline](docs/ci-cd.md) | GitHub Actions workflow and CI implementation |
| [Security Scan](docs/security-scan.md) | Trivy findings and security decisions |

## 11. Project Roadmap

The main portfolio version is being completed locally. Each milestone must be implemented, tested, documented, and verified before moving to the next. Real AWS deployment remains a later optional extension.

### Phase 0 — Application, Docker, CI, Security, and Database Reliability

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
- [x] Verify the final two-revision migration history against a fresh PostgreSQL database.
- [x] Verify FastAPI startup and API access against the fresh database.
- [x] Add the database readiness endpoint and automated success/failure tests.
- [x] Verify controlled PostgreSQL outage and recovery.
- [x] Verify PostgreSQL backup archive and isolated restore of all five tickets.
- [x] Synchronize project documentation and verify GitHub Actions.

### Phase 1 — Kubernetes with Minikube

- [ ] Inspect the existing Minikube cluster and Kubernetes context.
- [ ] Understand Kubernetes architecture, control plane, and worker nodes.
- [ ] Understand Pods and Deployments.
- [ ] Build the application image and make it available to Minikube.
- [ ] Deploy FastAPI and PostgreSQL using Kubernetes resources.
- [ ] Create Services and verify in-cluster communication.
- [ ] Configure namespaces, ConfigMaps, and Secrets.
- [ ] Configure PersistentVolumes and PersistentVolumeClaims for PostgreSQL.
- [ ] Configure liveness and readiness probes.
- [ ] Set resource requests and limits.
- [ ] Practise scaling and Horizontal Pod Autoscaling where supported.
- [ ] Verify application access and database persistence.

### Phase 2 — Helm

- [ ] Understand Helm charts and their structure.
- [ ] Learn templates, values, and chart metadata.
- [ ] Create a Helm chart for the application.
- [ ] Configure environment-specific values.
- [ ] Practise Helm install, upgrade, rollback, and uninstall.

### Phase 3 — Terraform and Infrastructure as Code Practice

- [ ] Understand Infrastructure as Code and Terraform.
- [ ] Learn providers, resources, data sources, variables, and outputs.
- [ ] Understand Terraform state and state management.
- [ ] Practise `terraform init`, `fmt`, `validate`, and `plan`.
- [ ] Practise safe apply and cleanup in a local or sandbox environment.
- [ ] Create a separate configuration and state for local practice.
- [ ] Keep the historical AWS Terraform configuration and state separate.

### Phase 4 — Ansible and Configuration Management

- [ ] Understand configuration management.
- [ ] Learn Ansible inventory and configuration.
- [ ] Learn playbooks, tasks, and modules.
- [ ] Understand variables, handlers, and templates.
- [ ] Learn Ansible roles.
- [ ] Practise configuration management in a local Linux environment.

### Phase 5 — GitOps with Argo CD

- [ ] Understand GitOps principles.
- [ ] Install Argo CD in the local Kubernetes cluster.
- [ ] Connect the application repository or deployment-manifest path.
- [ ] Configure an Argo CD application.
- [ ] Practise sync, drift detection, and self-healing.
- [ ] Practise deployment rollback and recovery.

### Phase 6 — Monitoring, Logging, and Observability

- [ ] Understand monitoring and observability fundamentals.
- [ ] Install Prometheus in the local cluster.
- [ ] Install Grafana and configure dashboards.
- [ ] Monitor application and Kubernetes metrics.
- [ ] Centralize application and container logs.
- [ ] Configure useful alerts.
- [ ] Practise troubleshooting using logs and metrics.

### Phase 7 — Reliability and Final Demonstration

- [ ] Introduce controlled application and infrastructure failures.
- [ ] Test container restart and recovery.
- [ ] Verify persistent data after failures.
- [ ] Practise backup and restore.
- [ ] Document troubleshooting and recovery procedures.
- [ ] Prepare architecture diagrams and deployment documentation.
- [ ] Rehearse a complete project demonstration.

### Phase 8 — Optional AWS Extension After Local Portfolio V1

- [ ] Review AWS account access, eligibility, and cost controls before any deployment.
- [ ] Revisit AWS IAM and least-privilege access.
- [ ] Review VPC, subnets, route tables, Internet Gateways, and security groups.
- [ ] Review EC2, ECR, RDS, ECS/EKS, and CloudWatch options.
- [ ] Reconcile the historical AWS Terraform configuration before any reuse.
- [ ] Estimate costs and plan cleanup before creating billable resources.
- [ ] Deploy to real AWS only when a suitable account and budget are available.

### Phase 9 — AI Capabilities and Architecture Evolution

- [ ] Evaluate AI-assisted ticket summarization.
- [ ] Explore ticket classification.
- [ ] Add knowledge-base assistance.
- [ ] Evaluate AI-generated troubleshooting suggestions.
- [ ] Measure the usefulness and reliability of AI features.
- [ ] Evaluate microservices only when justified by application requirements.

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
