# AI Helpdesk Copilot

A web-based IT support application designed to help support teams
create, manage, investigate, and resolve support tickets.

The project will demonstrate an end-to-end DevOps workflow by
building an application and progressively introducing automation,
cloud infrastructure, security, deployment, and observability.

## Project Status

**Current stage:** Requirements and project planning.

Application implementation has not started yet.

## Planned Features

- Ticket dashboard
- Create and view support tickets
- Filter tickets by status and priority
- Update ticket status and priority
- Persistent PostgreSQL database
- Backend health-check endpoint
- Troubleshooting suggestions and AI-assisted responses

## Planned Technology Stack

| Area | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Version Control | Git, GitHub |
| Containers | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS |
| Infrastructure as Code | Terraform |
| Configuration Management | Ansible |
| Container Orchestration | Kubernetes |
| Monitoring and Logging | CloudWatch and other appropriate tools |
| Security | Automated testing and DevSecOps practices |

## Planned Architecture

The initial application will have three main components:

1. **Frontend:** Provides the browser-based user interface.
2. **Backend:** Processes requests and implements application logic.
3. **Database:** Stores ticket information persistently.

The architecture will evolve as the project develops.

## Project Roadmap

- [x] Define initial project requirements
- [ ] Verify development environment
- [ ] Build the initial application
- [ ] Integrate PostgreSQL
- [ ] Add automated tests
- [ ] Containerize the application
- [ ] Build the CI/CD pipeline
- [ ] Deploy to AWS
- [ ] Automate infrastructure with Terraform
- [ ] Configure hosts with Ansible
- [ ] Deploy to Kubernetes
- [ ] Implement monitoring, logging, and alerting
- [ ] Practise failure injection and troubleshooting
- [ ] Evaluate and implement a microservices architecture

## Documentation

- [Project Requirements](docs/requirements.md)

## Learning Approach

This project follows a hands-on approach:

Understand the requirement, implement the solution, test it,
troubleshoot failures, document the result, and verify completion.

Features will be marked complete only after they have been implemented
and tested.