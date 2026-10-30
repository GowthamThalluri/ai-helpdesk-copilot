# AI Helpdesk Copilot — Project Progress

**Last updated:** 30 October 2026

## 1. Overall Project Status

The AI Helpdesk Copilot application has been implemented and verified locally using Docker Compose.

The project has completed the following major milestones:

- Application development and PostgreSQL integration.
- Automated application testing.
- Application hardening.
- Docker and Docker Compose.
- Continuous Integration using GitHub Actions.
- Dependency, source-code, secret, and container security scanning.
- Container runtime hardening.
- Security documentation.

**Current implementation stage:** Application + Docker + Continuous Integration + Security.

**Not yet implemented:** Continuous Delivery/Deployment to AWS.

The next technical phase is AWS fundamentals and project infrastructure architecture, followed by Terraform.

---

## 2. Application Development — Completed

### Frontend

- Created the dashboard using HTML and CSS.
- Implemented JavaScript for ticket creation, listing, filtering, and updates.
- Configured FastAPI to serve the frontend files and static assets.
- Verified that the dashboard loads through FastAPI.
- Tested ticket creation through the browser interface.
- Tested status filtering.
- Tested priority filtering.
- Tested combined status and priority filtering.
- Tested ticket status and priority updates through the UI.
- Verified that UI updates persist in PostgreSQL.

### Backend

- Created the FastAPI application.
- Implemented the backend health endpoint.
- Created ticket validation and response schemas.
- Implemented ticket creation.
- Implemented ticket listing and filtering.
- Implemented single-ticket retrieval.
- Implemented ticket status and priority updates.
- Added handling for nonexistent tickets.
- Added handling for invalid and empty update requests.
- Added whitespace trimming and validation.
- Documented appropriate HTTP error responses in the FastAPI OpenAPI specification.
- Added application logging using Python's built-in logging library.
- Added informational logs for ticket creation and updates.
- Added warning logs when a requested ticket is not found.
- Verified application logs through the running application's terminal.

### Database

- Integrated PostgreSQL with the FastAPI application.
- Installed and configured SQLAlchemy and Psycopg.
- Created the ticket database model.
- Configured PostgreSQL connections and database sessions.
- Configured environment variables for database connectivity.
- Verified ticket creation, retrieval, filtering, and updates.
- Verified ticket persistence after restarting the application.
- Verified database records directly through PostgreSQL.

---

## 3. Automated Testing — Completed

- Created `requirements-dev.txt`.
- Added API tests in `tests/test_tickets.py`.
- Configured an isolated in-memory SQLite database for testing.
- Ensured tests do not modify the real PostgreSQL database.
- Tested the health endpoint.
- Tested ticket creation and listing.
- Tested ticket filtering.
- Tested single-ticket retrieval.
- Tested ticket updates.
- Tested missing-ticket and invalid-request responses.
- Tested invalid priorities.
- Tested short titles and missing required fields.
- Tested whitespace-only titles, descriptions, and categories.
- Resolved the Starlette test-client deprecation warning by updating test dependencies.
- Verified dependencies using `python -m pip check`.
- Verified all tests using `python -m pytest -v`.

**Current verified local test result:** 15 passed.

---

## 4. Docker and Docker Compose — Completed

### Docker fundamentals and practical work

- Learned Docker images, containers, Docker client, daemon, registries, networks, port publishing, and persistent volumes.
- Inspected existing Docker images, containers, networks, logs, and container configuration.
- Diagnosed and recovered the existing PostgreSQL container without deleting its database volume.
- Verified that existing ticket records remained available after container recovery.

### Application containerization

- Renamed the backend directory from `app/` to `backend/`.
- Updated Python imports and the Uvicorn startup module.
- Created `.dockerignore` to exclude local secrets, virtual environments, test artifacts, Git metadata, and unnecessary files.
- Created a Dockerfile using `python:3.13-slim`.
- Configured the application to run as a non-root user.
- Installed application runtime dependencies during image construction.
- Removed pip from the final runtime image after dependency installation.
- Verified that pip is absent while the required application dependencies remain available.
- Built the application image with versioned tags, including `ai-helpdesk-copilot:1.0` and `ai-helpdesk-copilot:1.1`.

### Docker networking and persistence

- Configured application-to-PostgreSQL communication through Docker networking.
- Used the PostgreSQL service hostname for application database connectivity.
- Configured database environment variables.
- Reused the named volume `ai_helpdesk_pgdata`.
- Verified that existing ticket records survived container recovery.

### Docker Compose

- Created `compose.yaml` for the FastAPI application and PostgreSQL.
- Configured the application and database as separate services.
- Configured environment variables and published ports.
- Configured persistent database storage.
- Configured PostgreSQL health checks and service dependencies.
- Configured restart policies.
- Reused the existing external PostgreSQL volume to preserve database records.
- Migrated from manually managed containers to Compose-managed services.
- Verified that `docker compose config --quiet` succeeds.
- Verified that both services start successfully.
- Verified that PostgreSQL becomes healthy.
- Confirmed that the application is available at `127.0.0.1:8000`.
- Verified the `/health` endpoint.
- Confirmed that `GET /tickets` returns the expected ticket records.
- Verified that the dashboard displays ticket records after the Compose migration.
- Confirmed that all 15 automated tests pass after containerization.

**Status:** Dockerfile, application image, non-root runtime, networking, persistent storage, and Docker Compose implementation completed and verified.

---

## 5. Continuous Integration — Completed

**Tool:** GitHub Actions

Workflow file:

`.github/workflows/tests.yaml`

### Workflow triggers

- Push to `main`.
- Pull requests targeting `main`.

### Job 1 — Automated Testing

- Sets up Python 3.13.
- Installs development dependencies.
- Runs the automated Pytest suite.

### Job 2 — Dependency Audit

**Tool:** pip-audit

- Installs pip-audit.
- Scans the Python dependencies listed in `requirements-dev.txt`.
- Reports known dependency vulnerabilities.

### Job 3 — Repository Secret Scanning

**Tool:** Gitleaks

- Checks repository history for accidentally committed secrets.
- Uses full Git history during checkout.
- Configures secret scanning without automatic comments.

### Job 4 — Python Code Security

**Tool:** Bandit

- Installs Bandit.
- Scans the backend for common Python security issues.

### Job 5 — Docker Image Build and Security Scanning

**Tools:** Docker Buildx and Trivy

This job waits for all four preceding quality and security jobs to succeed.

Docker image build:

- Builds the Docker image using the repository Dockerfile.
- Tags the image as `ai-helpdesk-copilot:ci`.
- Loads the image into the GitHub Actions runner.
- Does not publish the image to an external registry.

Trivy scanning:

- Scans operating-system and application-library vulnerabilities.
- Generates a JSON vulnerability report.
- Uploads the report as a GitHub Actions artifact.
- Retains the artifact for 30 days.
- Runs a separate security gate for fixable HIGH and CRITICAL findings.
- Retains visibility of unfixed findings in the complete report.

### CI Verification

- Verified successful GitHub Actions execution.
- Tested an intentional automated-test failure through a pull request.
- Verified that the dependent Docker build job is skipped when a required check fails.
- Restored the test and verified successful execution.
- Added dependency auditing to CI.
- Added Gitleaks secret scanning.
- Added Bandit Python code scanning.
- Added Docker image building.
- Added Trivy vulnerability reporting and security gating.
- Verified successful Trivy-enabled GitHub Actions run #11.

**Latest specifically recorded Trivy-enabled workflow:** Run #11, commit `b137e01`, successful, duration 1 minute 28 seconds.

**Status:** Continuous Integration implemented and verified.

---

## 6. Container Security — Implemented, Findings Tracked

### Security tools

- pip-audit: Python dependency auditing.
- Gitleaks: repository secret scanning.
- Bandit: Python source-code security scanning.
- Trivy: Docker image vulnerability scanning.

### Runtime image hardening

- Investigated Python vulnerability findings reported by Trivy.
- Found the reported package versions in pip's embedded SBOM.
- Verified that those packages were not independently installed as application distributions.
- Removed pip from the runtime image after application dependency installation.
- Verified that pip was unavailable in the image.
- Verified that FastAPI, Uvicorn, SQLAlchemy, Psycopg, and dotenv remained importable.
- Rebuilt the image without using build cache.
- Reran Trivy and verified that Python package findings were no longer reported.

### Remaining Debian findings

The subsequent Trivy scan reported:

- 44 HIGH Debian package vulnerability entries.
- 0 CRITICAL Debian findings.
- 0 Python package findings.

The 44 Debian entries contain repeated package/CVE combinations. They are not 44 distinct CVEs.

The image uses Debian 13 (Trixie).

During investigation:

- Checked package versions using `apt-cache policy`.
- Checked `util-linux`, `libacl1`, `ncurses-base`, `libsystemd0`, and `perl-base`.
- Found that the configured repositories did not offer newer candidate versions for the checked packages.
- Kept the findings visible instead of suppressing them.
- Avoided mixing packages from unsupported or testing Debian releases into the application image.

These Debian findings remain unresolved and must not be marked as fixed.

### Trivy CI policy

The complete Trivy scan:

- Includes HIGH and CRITICAL findings.
- Includes findings without an available fix.
- Generates a JSON report.
- Uploads the report as a workflow artifact.

The separate security gate:

- Ignores findings Trivy classifies as unfixed for blocking purposes.
- Fails for fixable HIGH and CRITICAL findings.

A successful gate is not proof that the image contains zero vulnerabilities.

### Security documentation

Created and published:

`docs/security-scan.md`

The document records:

- Scanner information.
- Initial and subsequent scan results.
- Runtime image hardening.
- Debian vulnerability assessment.
- CI gate policy.
- Follow-up actions.

**Status:** Security scanning implemented; unresolved Debian findings documented and tracked.

---

## 7. Repository Documentation

The project documentation consists of:

| File | Purpose |
|---|---|
| `README.md` | Project overview, features, setup instructions, and roadmap |
| `docs/requirements.md` | Original project requirements |
| `docs/progress.md` | Completed work, current status, and roadmap |
| `docs/ci-cd.md` | GitHub Actions pipeline and CI implementation |
| `docs/security-scan.md` | Trivy findings and container security decisions |

The current documentation cleanup includes updating the README, adding CI/CD documentation, and reconciling this progress record.

---

## 8. Current Limitations and Pending Work

### Application improvements

- Additional database failure and transaction-rollback testing.
- Automated browser/UI testing.
- Database schema migrations.

### Continuous Delivery/Deployment

- Publish the verified Docker image to Amazon ECR.
- Configure secure AWS authentication for GitHub Actions.
- Deploy the application to an appropriate AWS runtime.
- Automate deployment through GitHub Actions.
- Add deployment health verification.
- Practise rollout and rollback procedures.

### AWS infrastructure

- Prepare the AWS infrastructure architecture.
- Review IAM and least-privilege access.
- Plan VPC, subnets, routing, security groups, and network access.
- Evaluate EC2 and appropriate application hosting choices.
- Understand ECR and CloudWatch.
- Establish resource cost and cleanup controls.

### Infrastructure as Code

- Learn Terraform fundamentals.
- Manage AWS resources using Terraform.
- Understand Terraform state and state management.
- Organize reusable infrastructure configurations.

### Configuration management

- Learn Ansible inventory, playbooks, variables, handlers, and roles.
- Automate configuration tasks where required by the deployment architecture.

### Kubernetes and Helm

- Learn Kubernetes using Minikube.
- Implement Pods, Deployments, Services, and ReplicaSets.
- Learn ConfigMaps and Secrets.
- Configure health probes and resource requests and limits.
- Practise scaling and troubleshooting.
- Package the application using Helm.
- Evaluate EKS after local Kubernetes fundamentals and AWS cost planning.

### Monitoring and reliability

- Implement application and infrastructure monitoring.
- Configure metrics, dashboards, and alerts.
- Improve centralized logging.
- Practise failure injection and service recovery.

### AI capabilities

AI-assisted ticket summarization, classification, and knowledge assistance are planned for the final project stage.

---

## 9. Fixed Project Roadmap

The following sequence is the agreed implementation order. A milestone will not be marked complete until it has been implemented, tested, documented, and verified.

### Phase 0 — Repository Documentation and Setup

- [x] Create project requirements documentation.
- [x] Create security scan documentation.
- [x] Prepare CI/CD pipeline documentation.
- [x] Update the project README.
- [x] Reconcile the project progress record.
- [x] Add `.env.example` with safe placeholder values.
- [ ] Verify fresh-clone setup instructions.
- [ ] Review and publish the documentation changes together.
- [ ] Verify GitHub repository synchronization and Actions results.

### Phase 1 — AWS Fundamentals and Architecture

- [ ] Review AWS Regions and Availability Zones.
- [ ] Review IAM users, roles, policies, and least privilege.
- [ ] Understand VPC architecture.
- [ ] Understand public and private subnets.
- [ ] Learn route tables, internet gateways, and NAT.
- [ ] Understand security groups and network access.
- [ ] Evaluate EC2 and application hosting choices.
- [ ] Understand Amazon ECR for container images.
- [ ] Review CloudWatch and secrets management.
- [ ] Plan resource costs, cleanup, and security controls.

### Phase 2 — Terraform and Infrastructure as Code

- [ ] Understand Infrastructure as Code and Terraform.
- [ ] Learn Terraform providers.
- [ ] Learn resources and data sources.
- [ ] Learn variables and outputs.
- [ ] Understand Terraform state and state management.
- [ ] Practise `terraform init`.
- [ ] Practise `terraform fmt`.
- [ ] Practise `terraform validate`.
- [ ] Understand and inspect `terraform plan`.
- [ ] Practise `terraform apply`.
- [ ] Practise safe resource destruction using `terraform destroy`.
- [ ] Organize reusable Terraform configurations.
- [ ] Provision the required AWS project infrastructure.

### Phase 3 — Ansible and Configuration Management

- [ ] Understand configuration management.
- [ ] Learn Ansible inventory.
- [ ] Practise ad-hoc commands.
- [ ] Learn playbooks.
- [ ] Learn variables and handlers.
- [ ] Learn roles.
- [ ] Automate required host-configuration tasks.
- [ ] Integrate Ansible where appropriate for the chosen deployment architecture.

### Phase 4 — Complete Continuous Delivery/Deployment

- [ ] Publish verified application images to Amazon ECR.
- [ ] Configure secure AWS authentication for GitHub Actions.
- [ ] Prepare the deployment target.
- [ ] Deploy the application to the chosen AWS runtime.
- [ ] Automate deployment through GitHub Actions.
- [ ] Add deployment health checks.
- [ ] Verify successful application deployment.
- [ ] Practise rollback and recovery procedures.

### Phase 5 — Kubernetes and Helm

- [ ] Learn Kubernetes architecture and components.
- [ ] Understand Pods and ReplicaSets.
- [ ] Implement Deployments.
- [ ] Implement Services.
- [ ] Learn Kubernetes networking.
- [ ] Learn ConfigMaps and Secrets.
- [ ] Configure readiness and liveness probes.
- [ ] Configure resource requests and limits.
- [ ] Practise scaling.
- [ ] Troubleshoot failed Pods and Deployments.
- [ ] Learn Helm charts and values.
- [ ] Deploy the application using Helm.
- [ ] Evaluate Amazon EKS with appropriate cost and security controls.

### Phase 6 — Monitoring, Logging, and Reliability

- [ ] Implement application monitoring.
- [ ] Implement infrastructure monitoring.
- [ ] Configure metrics and dashboards.
- [ ] Implement useful alerts.
- [ ] Improve centralized log collection.
- [ ] Practise troubleshooting.
- [ ] Practise failure injection and service recovery.

### Phase 7 — Application and Architecture Evolution

- [ ] Evaluate microservices only when justified by application requirements.
- [ ] Implement AI-assisted ticket classification.
- [ ] Add ticket summarization.
- [ ] Develop a knowledge assistant using an appropriate retrieval architecture.

---

## 10. Development Environment Rules

- Use VS Code for editing.
- Use Windows Git Bash for Git and project commands.
- Use the Windows Python virtual environment for Python development.
- Use Docker Desktop for local containers and PostgreSQL.
- Keep `.env` files and credentials out of Git.
- Do not use Ubuntu/WSL for this project unless a requirement justifies it and the approach is reviewed first.
- Use AWS resources carefully.
- Avoid unnecessary paid resources.
- Clean up temporary cloud infrastructure when it is no longer required.

---

## 11. Working Rules for Every Milestone

Every milestone follows the same process:

1. Understand the concept before running commands.
2. Explain why the tool is needed and how it applies to this project.
3. Implement one bounded task at a time.
4. Test the implementation.
5. Troubleshoot failures and understand their causes.
6. Update the relevant project documentation.
7. Review the Git diff.
8. Commit and push verified changes to GitHub.
9. Verify repository synchronization and GitHub Actions.
10. Proceed only after the milestone is confirmed complete.

A tool is not considered completed merely because its commands or configuration files exist. It must be implemented in the project and verified.

---

**Current position:** Application development + PostgreSQL + Docker + Docker Compose + Continuous Integration + security scanning completed.

**Immediate pending work:** Finalize repository documentation, add `.env.example`, and verify a fresh-clone setup.

**Next technical phase:** AWS fundamentals and project infrastructure architecture, followed by Terraform.