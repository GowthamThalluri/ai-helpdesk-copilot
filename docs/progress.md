# AI Helpdesk Copilot — Project Progress

**Last updated:** 12 November 2026

## 1. Overall Project Status

The AI Helpdesk Copilot application is implemented and runs locally using Docker Compose. Application testing, database migrations, container security scanning, and the database reliability exercises recorded in this document have been verified.

The main portfolio version is now being completed locally. The next major phase is deploying the existing application to Kubernetes using the existing Minikube installation. Real AWS deployment is deferred until after the local portfolio version is complete.

### Completed major milestones

- Application development and PostgreSQL integration.
- Application validation, logging, and error responses.
- Dockerfile, non-root container runtime, and Docker Compose.
- Alembic database migrations and Docker Compose migration integration.
- Fresh-database migration and application startup verification.
- 17 automated API tests.
- GitHub Actions Continuous Integration.
- Dependency, source-code, secret, and container security scanning.
- Trivy Docker image security fix for the two recorded HIGH `zlib1g` findings.
- Database liveness/readiness checks.
- Controlled PostgreSQL outage and recovery verification.
- PostgreSQL backup archive inspection and isolated restore verification.
- Preservation of all five original ticket records.
- Terraform AWS network foundation committed as historical project work.

**Current implementation stage:** Local application + Docker Compose + database migrations + CI/security + database reliability verification.

**Next major phase:** Kubernetes deployment with Minikube.

**Cloud status:** No active AWS deployment is part of the current project phase. Existing AWS/Terraform work is preserved for a later optional extension. Do not run the historical AWS Terraform state against another account or environment.

---

## 2. Application Development — Completed

### Frontend

- Created the dashboard using HTML and CSS.
- Implemented JavaScript for ticket creation, listing, filtering, and updates.
- Configured FastAPI to serve the frontend files and static assets.
- Verified that the dashboard loads through FastAPI.
- Tested ticket creation through the UI.
- Tested status filtering and priority filtering.
- Tested combined filtering.
- Tested ticket status and priority updates through the UI.
- Verified that UI changes persist in PostgreSQL.

### Backend

- Implemented the FastAPI application.
- Implemented ticket creation and listing.
- Implemented ticket filtering and single-ticket retrieval.
- Implemented ticket status and priority updates.
- Added handling for nonexistent tickets and invalid requests.
- Added validation for missing and invalid input values.
- Configured the application to serve frontend static assets.
- Added `/health` to report whether the FastAPI process is responding.
- Added `/ready` to check whether PostgreSQL is reachable.

### Application Logging and Hardening

- Added Python logging using the standard logging library.
- Added informational logs for ticket creation and updates.
- Added warning logs for requested tickets that do not exist.
- Added whitespace trimming and input validation.
- Documented appropriate HTTP error responses in the FastAPI OpenAPI specification.
- Logged readiness-check database failures without returning internal database details to clients.

**Status:** Application implementation and hardening completed for the current V1 scope.

---

## 3. PostgreSQL and Database Integration — Completed

### Database

- Integrated PostgreSQL with FastAPI.
- Installed and configured SQLAlchemy.
- Installed and configured Psycopg.
- Created the SQLAlchemy ticket model.
- Configured PostgreSQL connections and database sessions.
- Configured environment variables for database connectivity.
- Configured the application to use the PostgreSQL service hostname in Docker.
- Implemented persistent ticket storage.
- Verified ticket creation, retrieval, filtering, and updates.
- Verified database records directly through PostgreSQL.
- Verified ticket persistence after application and container restarts.

### Existing Database

The original PostgreSQL database uses:

- Database: `helpdesk_db`
- Table: `tickets`
- Existing records: 5

The original database schema was inspected before introducing Alembic. The inspection confirmed seven ticket columns, an integer primary key, a PostgreSQL sequence for automatic ID generation, a timestamp-with-time-zone column for `created_at`, a primary-key index, and an additional secondary index named `ix_tickets_id`.

### Database Backup Before Migration

Before modifying the original database schema:

- Created a PostgreSQL custom-format backup.
- Validated the backup using `pg_restore --list`.
- Copied the backup outside the Docker container.
- Verified that the original and copied backup SHA-256 checksums matched.
- Kept the backup outside the Git repository.

**Status:** PostgreSQL integration and persistence completed. Existing records preserved.

---

## 4. Automated Testing — Completed

- Created `requirements-dev.txt`.
- Added automated API tests in `tests/test_tickets.py`.
- Configured an isolated in-memory SQLite database for testing.
- Ensured tests do not modify the real PostgreSQL database.
- Tested the liveness endpoint.
- Tested readiness when the database is available.
- Tested readiness returning HTTP 503 for a simulated SQLAlchemy database error.
- Tested ticket creation, listing, and filtering.
- Tested single-ticket retrieval and updates.
- Tested missing-ticket and invalid-request responses.
- Tested invalid priorities and invalid status filters.
- Tested short titles, missing required fields, and whitespace-only inputs.
- Resolved the Starlette test-client deprecation warning by updating test dependencies.
- Verified dependencies using `python -m pip check`.

**Latest verified result:**

```text
17 passed
```

The tests were executed using:

```bash
python -m pytest -q
```

**Status:** All 17 automated tests passed locally. GitHub Actions also passed after the readiness changes.

---

## 5. Docker and Docker Compose — Completed

### Docker Fundamentals and Practical Work

- Learned Docker images, containers, Docker client, daemon, registries, networks, port publishing, and persistent volumes.
- Inspected existing Docker images, containers, networks, logs, and container configuration.
- Diagnosed and recovered the existing PostgreSQL container without deleting its database volume.
- Verified that existing ticket records remained available after container recovery.

### Application Containerization

- Renamed the backend directory from `app/` to `backend/`.
- Updated Python imports and the Uvicorn startup module.
- Created `.dockerignore` to exclude local secrets, virtual environments, test artifacts, Git metadata, and unnecessary files.
- Created a Dockerfile using `python:3.13-slim`.
- Configured the application to run as a non-root user.
- Installed application dependencies during image construction.
- Removed pip from the final runtime image after dependency installation.
- Verified that pip is absent while required application dependencies remain available.
- Built versioned application images, including `ai-helpdesk-copilot:1.0`, `:1.1`, and the locally verified security-fix image `:1.2`.
- Added retry and timeout settings to Docker dependency installation.
- Explicitly configured the official PyPI package index for image builds.
- Updated Debian `zlib1g` to the fixed package version after Trivy identified two fixable HIGH findings.

### Docker Networking and Persistence

- Configured application-to-PostgreSQL communication through Docker networking.
- Used the PostgreSQL service hostname for application database connectivity.
- Configured database environment variables.
- Reused the named volume `ai_helpdesk_pgdata`.
- Verified that existing ticket records survived container recovery and restart.

### Docker Compose

- Created `compose.yaml` for the FastAPI application and PostgreSQL.
- Configured the application and database as separate services.
- Added a one-off `migrate` service for Alembic.
- Configured environment variables and published ports.
- Configured persistent database storage.
- Configured PostgreSQL health checks, service dependencies, and restart policies.
- Reused the existing external PostgreSQL volume to preserve database records.
- Verified that `docker compose config --quiet` succeeds.
- Verified PostgreSQL becomes healthy.
- Confirmed the application is available at `127.0.0.1:8000`.
- Verified `/health`, `/ready`, and `GET /tickets` through the running Compose application.

**Status:** Dockerfile, image build, non-root runtime, networking, persistent storage, and Docker Compose implementation completed.

---

## 6. Database Schema Migrations Using Alembic — Implemented and Verified

### Why Migrations Were Needed

A fresh PostgreSQL database did not automatically contain the `tickets` table. Database migrations were introduced to make schema creation and future schema changes version-controlled and repeatable.

### Alembic Configuration

- Added Alembic to `requirements.txt`.
- Initialized Alembic using `alembic init migrations`.
- Configured `migrations/env.py`.
- Connected Alembic to the application's SQLAlchemy engine.
- Configured `Base.metadata` as the migration target metadata.
- Enabled column-type comparison using `compare_type=True`.
- Added `alembic.ini`.
- Created version-controlled migration scripts.

### Migration History

Two migration revisions are currently implemented.

| Revision | Description |
|---|---|
| `e91d904ff8b7` | Create the tickets table and historical secondary index |
| `f1b9ab28aaf3` | Remove the redundant tickets ID index |

The original SQLAlchemy model explicitly requested an additional index on the primary-key column through `index=True`. PostgreSQL already creates an index for a primary key, so the unnecessary secondary index was removed from the current model. The migration history preserves the original schema as Revision 1 and removes the redundant index through Revision 2.

### Fresh-Database Migration and Application Verification — 12 November 2026

A separate temporary PostgreSQL database was used to verify the complete migration sequence without modifying the existing application database.

- Confirmed that the temporary database initially contained no tables.
- Executed `alembic upgrade head` using the application Docker image.
- Verified revisions `e91d904ff8b7` and `f1b9ab28aaf3` ran successfully in order.
- Confirmed `alembic current` reported `f1b9ab28aaf3 (head)`.
- Inspected the resulting `tickets` table and confirmed its seven columns and primary-key index.
- Started a separate FastAPI container against the migrated database.
- Verified `GET /health` returned HTTP 200 with `{"status":"healthy"}`.
- Verified `GET /tickets` returned HTTP 200 with an empty list, as expected for a fresh database.
- Removed only the temporary containers, temporary anonymous volume, and test network.
- Rechecked the original Compose application: PostgreSQL remained healthy, FastAPI returned HTTP 200, and all five original tickets remained present.

**Status:** Fresh-database migration and application startup verification completed.

### Docker Compose Migration Integration

The Dockerfile includes `migrations/` and `alembic.ini`. The Compose configuration contains a dedicated migration service that runs `alembic upgrade head`. The FastAPI application depends on the migration service completing successfully.

The deployment sequence is:

```text
PostgreSQL starts
      |
      v
PostgreSQL health check passes
      |
      v
Alembic migration service runs
      |
      v
Migration exits successfully
      |
      v
FastAPI starts
```

The migration service is a one-time task. An exit status of `0` indicates success.

### Existing Database Baseline

The original PostgreSQL database already contained the tickets table and five records. Running the initial `CREATE TABLE` migration directly against this database would have failed because the table already existed.

The existing database was inspected and backed up before migration. The baseline was recorded using:

```bash
alembic stamp e91d904ff8b7
```

This recorded Revision 1 without executing its table-creation operation. The next migration was applied using:

```bash
alembic upgrade head
```

Only Revision 2 executed against the existing database.

### Final Original Database Verification

The final verification confirmed:

```text
Ticket count: 5
Alembic revision: f1b9ab28aaf3
Tables: tickets, alembic_version
```

The primary key remained in place, the redundant secondary index was removed, and all five existing ticket records were preserved.

**Status:** Alembic implementation, existing-database baseline, fresh-database migration, and original database preservation verified.

---

## 7. Database Readiness, Outage, Recovery, and Backup/Restore — Verified

This DevOps reliability milestone was completed on 12 November 2026.

### Readiness Endpoint

- Added `GET /ready` to execute a lightweight database query.
- Returns HTTP 200 with `{"status":"ready","database":"connected"}` when PostgreSQL is reachable.
- Returns HTTP 503 with a controlled `Database unavailable` response when a SQLAlchemy database error occurs.
- Added automated tests for both successful readiness and simulated database failure.

### Controlled PostgreSQL Outage and Recovery

- Confirmed `/health` and `/ready` returned HTTP 200 while PostgreSQL was healthy.
- Stopped only the PostgreSQL Compose service using `docker compose stop postgres`.
- Confirmed FastAPI remained running and `/health` returned HTTP 200.
- Confirmed `/ready` returned HTTP 503 while PostgreSQL was stopped.
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
- Restored the backup into the empty temporary database using `pg_restore`.
- Verified that the restored database contained five tickets.
- Verified the restored Alembic revision was `f1b9ab28aaf3`.
- Removed only the temporary restore container and its anonymous volume.
- Rechecked the original database and confirmed all five original tickets were still present.

**Status:** Readiness behavior, database outage/recovery, backup archive inspection, and isolated restore verification completed. The original database volume was not overwritten or deleted.

---

## 8. Continuous Integration — Implemented

The project uses GitHub Actions for automated checks.

### CI Jobs

1. **Test:** Runs automated application tests.
2. **Dependency Audit:** Uses pip-audit to identify vulnerable dependencies.
3. **Secret Scan:** Uses Gitleaks to scan repository history.
4. **Bandit Scan:** Checks Python source code for security issues.
5. **Build Image:** Builds and scans the Docker image after the preceding quality and security jobs succeed.

The image build uses a non-publishing configuration. Docker images are built and scanned but are not pushed to Amazon ECR or another external registry.

### Latest GitHub Actions Verification

- Latest implementation commit: `89567e6`.
- Branch: `main`.
- Result: Successful, as confirmed after the readiness and test changes.

Earlier successful Trivy workflow verification:

- Commit: `b98883f`.
- Workflow run: #19.
- Duration: 1 minute 31 seconds.
- Artifacts: 3.

**Status:** Continuous Integration implemented and the latest readiness implementation commit verified successfully by GitHub Actions. Continuous Delivery/Deployment remains unimplemented.

---

## 9. Security and Container Hardening — Implemented

### Dependency Security

- Added pip-audit to the CI pipeline.
- Configured automated dependency auditing.

### Source Code Security

- Added Bandit.
- Configured automated Python source-code security checks.

### Secret Security

- Added Gitleaks.
- Configured repository-history secret scanning.
- Added `.env` to `.gitignore`.
- Added `.env.example` with safe placeholder values.

### Container Security

- Added Trivy image vulnerability scanning.
- Configured JSON vulnerability report generation and artifact retention.
- Configured a CI gate for fixable HIGH and CRITICAL findings.
- Updated Debian `zlib1g` after Trivy identified two fixable HIGH findings: `CVE-2026-76844` and `CVE-2026-85091`.
- Verified the fixed package version in the locally rebuilt image.
- Removed pip from the final runtime image.
- Configured a non-root application user.

GitHub Actions Run #19 passed the Trivy blocking gate after the zlib update. A successful Trivy gate does not mean that the image has zero known vulnerabilities; the complete report remains the reference for findings that are not blocked by the configured policy.

See `docs/security-scan.md` for the recorded findings and decisions.

**Status:** Security checks and container hardening implemented. Remaining findings are documented and tracked.

---

## 10. Terraform AWS Network Foundation — Preserved for Later

Terraform configuration for the previous personal AWS environment was committed in the repository. It describes a VPC, six subnets, an Internet Gateway, route tables, and security groups.

- Commit: `4934361` — `Add Terraform AWS network foundation`.
- The Terraform configuration was formatted and validated.
- A Terraform plan reported no changes against the then-existing AWS environment.
- Terraform state and provider binaries were excluded from Git.
- The AWS account was subsequently closed by the user.

**Current decision:** Preserve the Terraform files as project history. Do not run `terraform apply` using the old configuration or state. Real AWS deployment is deferred until after the local portfolio version is complete. Terraform learning and practice will use a separate local or sandbox configuration and separate state.

### AWS Fundamentals — Day 1 Completed (Historical Learning)

Topics covered:

- AWS Regions.
- Availability Zones.
- Multi-AZ architecture and high availability.
- Load balancing and application availability.
- Edge Locations.
- Amazon CloudFront.
- Cache hits, cache misses, and origin retrieval.

**Status:** Conceptual learning completed. Real AWS deployment is deferred until after the local portfolio version is complete.

---

## 11. Repository Documentation

The project documentation consists of:

| File | Purpose |
|---|---|
| `README.md` | Project overview, features, setup instructions, and roadmap |
| `docs/requirements.md` | Original application requirements |
| `docs/progress.md` | Completed work, current status, and roadmap |
| `docs/ci-cd.md` | GitHub Actions pipeline and CI implementation |
| `docs/security-scan.md` | Trivy findings and container security decisions |

### Documentation Status

- Updated README with application architecture and database migration instructions.
- Documented Alembic migration revisions and Docker Compose integration.
- Documented CI and security implementation.
- Recorded the fresh-database migration verification.
- Recorded readiness, outage/recovery, and backup/restore exercises.
- Recorded the local-first project direction and deferred AWS extension.

**Status:** This documentation update is prepared for review, commit, and push.

---

## 12. Current Limitations and Pending Work

### Application Improvements

- Automated browser/UI testing.
- Additional application-level failure scenarios where useful.
- Final project demonstration and documentation polish.

### Kubernetes and Helm

- Inspect the existing Minikube cluster.
- Deploy the FastAPI application and PostgreSQL using Kubernetes resources.
- Configure Services, ConfigMaps, Secrets, and persistent storage.
- Configure liveness and readiness probes.
- Configure resource requests, limits, and autoscaling.
- Package the application with Helm.

### Terraform and Ansible Practice

- Create a separate local Terraform configuration and state for practice.
- Learn Terraform variables, outputs, resources, providers, and state handling.
- Practise Ansible inventory, playbooks, tasks, variables, handlers, and roles in a local Linux environment.

### GitOps

- Install Argo CD in the local Kubernetes cluster.
- Connect the repository deployment manifests.
- Practise sync, drift detection, self-healing, and rollback.

### Monitoring and Reliability

- Install Prometheus and Grafana locally.
- Add application and infrastructure dashboards.
- Centralize useful application and container logs.
- Configure alerts and practise troubleshooting.
- Perform additional controlled failure and recovery exercises.

### Later Optional AWS Extension

Real AWS deployment, Amazon ECR publishing, AWS authentication for GitHub Actions, and AWS-hosted infrastructure are deferred until after the local portfolio version is complete.

### AI Capabilities

AI-assisted ticket summarization, classification, and knowledge assistance are planned for a later project stage.

---

## 13. Fixed Project Roadmap

The main portfolio version is being completed locally. A milestone will not be marked complete until it has been implemented, tested, documented, and verified.

### Phase 0 — Application, Docker, CI, Security, and Database Reliability

- [x] Create project requirements documentation.
- [x] Implement the application and PostgreSQL integration.
- [x] Implement automated application testing.
- [x] Implement Docker and Docker Compose.
- [x] Implement Continuous Integration.
- [x] Implement dependency, source-code, secret, and container security scanning.
- [x] Document container security findings.
- [x] Implement Alembic database migrations.
- [x] Integrate automatic migrations into Docker Compose startup.
- [x] Safely baseline the existing PostgreSQL database.
- [x] Preserve all five existing tickets during migration.
- [x] Verify the original application after migration.
- [x] Verify the final two-revision migration history against a fresh PostgreSQL database.
- [x] Verify FastAPI startup and API access against the fresh database.
- [x] Add the database readiness endpoint and automated success/failure tests.
- [x] Verify controlled PostgreSQL outage and recovery.
- [x] Verify PostgreSQL backup archive and isolated restore of all five tickets.
- [x] Verify GitHub Actions after the readiness and test changes.

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

---

## 14. Working Rules

For every project milestone:

1. Understand the requirement.
2. Learn the underlying concepts.
3. Implement the task.
4. Test the result.
5. Troubleshoot failures.
6. Document the outcome.
7. Commit and push the verified change.
8. Confirm the relevant GitHub Actions result before proceeding.

### Development Environment Rules

- Use VS Code for editing.
- Use Windows Git Bash for Git and development commands.
- Use the Windows Python virtual environment for Python development.
- Use Docker Desktop for containers and PostgreSQL.
- Use the existing Minikube installation for local Kubernetes practice.
- Keep `.env` and all credentials out of Git.
- Do not delete persistent database volumes unless explicitly intended.
- Back up existing databases before schema migrations.
- Do not mark a task complete without verification.
- Do not run the historical AWS Terraform configuration against another account or environment.
- Do not advance to the next major project phase until the current phase is complete.
