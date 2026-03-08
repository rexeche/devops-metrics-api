# DevOps Metrics API

A Python REST API for tracking DORA deployment metrics — built as a hands-on DevOps portfolio project to demonstrate end-to-end infrastructure and CI/CD skills on AWS.

> The application is intentionally simple. The point is everything around it.

## What This Demonstrates

- **Containerization** — Multi-stage Docker build with non-root user and health checks
- **Kubernetes on AWS EKS** — Deployments, Services, namespaces, and Horizontal Pod Autoscaler across dev/staging/production environments
- **CI/CD with GitHub Actions** — Full pipeline: lint → test → build → push → deploy to staging → approval gate → deploy to production
- **Infrastructure as Code** — AWS infrastructure (EKS cluster, VPC, ECR) provisioned with Terraform using a modular, environment-separated structure
- **Container security** — Trivy vulnerability scanning integrated into the CI pipeline
- **Environment promotion** — Automated staging deploy with smoke tests, manual approval gate before production

## Tech Stack

| Layer | Tool |
|-------|------|
| Application | Python 3.11 + FastAPI |
| Containerization | Docker (multi-stage builds) |
| Orchestration | Kubernetes on AWS EKS |
| Container Registry | AWS ECR |
| Infrastructure | Terraform |
| CI/CD | GitHub Actions |
| Security Scanning | Trivy |

## The API

Tracks the four [DORA metrics](https://dora.dev) used to measure software delivery performance:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/deployments` | POST | Record a deployment event |
| `/deployments` | GET | List deployments (filterable by service/environment) |
| `/metrics/{service_name}` | GET | Get aggregated metrics for a service |

## Pipeline

```
Push to main
    │
    ▼
CI Pipeline (ci.yml)
├── Lint (flake8)
├── Test (pytest)
├── Build & push Docker image to GHCR
└── Trivy security scan
    │
    ▼
Deploy Pipeline (deploy.yml)
├── Build & push image to ECR (tagged with commit SHA)
├── Deploy to staging (devops-metrics-staging namespace)
├── Smoke test staging
├── [Manual approval gate] ◄── required reviewer
└── Deploy to production (devops-metrics-production namespace)
    └── Smoke test production
```

## Infrastructure

Terraform provisions:
- **VPC** with public/private subnets across 2 availability zones
- **EKS cluster** (Kubernetes 1.29) with managed node group
- **ECR repository** with image scanning and lifecycle policy

```
terraform/
├── environments/
│   └── dev/
└── modules/
    ├── eks/
    └── ecr/
```

## Kubernetes Structure

Three environment namespaces on a single cluster, each with different resource profiles:

```
k8s/
├── dev/          # manual deploys, sandbox
├── staging/      # 1 replica, reduced resources, auto-deployed from main
└── production/   # 2 replicas, HPA (scales 2–5 pods at 70% CPU), gated deploy
```

## Running Locally

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
uvicorn app.main:app --reload --port 8000
```

```bash
docker build -t devops-metrics-api:latest .
docker run -p 8000:8000 devops-metrics-api:latest
```