# Docker + Kubernetes + GitHub Actions CI/CD

A DevOps portfolio project demonstrating a development-to-production workflow using Docker, Kubernetes, GitHub Actions and GitHub Container Registry (GHCR).

## Architecture

Developer -> `dev` branch -> GitHub Actions -> Docker image -> GHCR -> temporary Kind Kubernetes cluster -> Dev namespace

Developer -> Pull Request `dev` -> `main` -> Review/Approval -> GitHub Actions -> Docker image -> GHCR -> temporary Kind Kubernetes cluster -> Prod namespace

> The CI workflows use an ephemeral Kubernetes cluster created inside the GitHub Actions runner. This makes the demo fully testable without an Azure/AWS/GCP Kubernetes cluster.

## Local Docker test

```bash
docker build -t devops-demo:local .
docker run -p 5000:5000 -e APP_ENV=local devops-demo:local
```

Open `http://localhost:5000` and `http://localhost:5000/health`.

## Kubernetes

Apply namespaces:

```bash
kubectl apply -f k8s/namespaces.yaml
```

Development:

```bash
kubectl apply -f k8s/dev/
kubectl -n dev get pods
kubectl -n dev get svc
kubectl -n dev port-forward svc/demo-app 8080:80
```

Production:

```bash
kubectl apply -f k8s/prod/
kubectl -n prod get pods
kubectl -n prod get svc
```

## Git workflow

- `dev` is the development branch.
- A push to `dev` triggers the development CI/CD workflow.
- A pull request is created from `dev` to `main`.
- `main` is the production branch and should be protected with required review.
- A merge to `main` triggers the production workflow.

## GitHub Actions

Workflows:

- `.github/workflows/dev.yml` - development CI/CD
- `.github/workflows/prod.yml` - production CI/CD

Each workflow:
1. Checks out the code.
2. Installs Python dependencies and validates the application.
3. Builds a Docker image.
4. Pushes the image to GHCR.
5. Pulls the image into the GitHub runner.
6. Creates an ephemeral Kubernetes cluster using Kind.
7. Loads the image into the cluster.
8. Deploys the appropriate Kubernetes manifests.
9. Waits for the Deployment rollout and displays Pods/Services.

No `KUBE_CONFIG` secret is required for this demo because the Kubernetes cluster is created inside the same GitHub Actions runner.

## Branch protection

For `main`, configure:

- Require a pull request before merging
- Require at least 1 approval
- Require successful status checks where appropriate
- Restrict direct pushes

See `docs/branch-protection.md`.

## What this project demonstrates

- Docker image creation and containerization
- Kubernetes Deployments and Services
- Separate dev and prod namespaces
- GitHub Actions CI/CD
- GitHub Container Registry
- Ephemeral Kubernetes testing with Kind
- Pull-request promotion from `dev` to `main`
- Kubernetes readiness/liveness probes and resource limits
- Environment-specific configuration

## Interview explanation

"I created a DevOps CI/CD project where the dev branch is used for development and main is protected for production. A push to dev triggers GitHub Actions, which validates the application, builds a Docker image, pushes it to GHCR, creates a temporary Kind Kubernetes cluster, loads the image into the cluster and deploys it to the development namespace. For production, changes are promoted through a pull request from dev to main. After review and approval, merging to main triggers a separate workflow that performs the same build and deployment process in the production namespace. I kept dev and prod isolated using separate Kubernetes namespaces."

## Important note

This is a CI/CD portfolio demonstration. The Kubernetes clusters created by GitHub Actions are temporary and exist only for the duration of each workflow run. For a real production system, the Kind cluster should be replaced with a persistent AKS, EKS, GKE or other managed Kubernetes cluster.
