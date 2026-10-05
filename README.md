# Docker + Kubernetes + GitHub Actions CI/CD

A simple DevOps portfolio project demonstrating a development-to-production workflow using Docker, Kubernetes and GitHub Actions.

## Architecture

Developer -> `dev` branch -> GitHub Actions -> Docker image -> GHCR -> Dev Kubernetes environment

Developer -> Pull Request `dev` -> `main` -> Review/Approval -> GitHub Actions -> Docker image -> GHCR -> Production Kubernetes environment

## Project requirements

- Docker
- Kubernetes cluster (Minikube, Kind, AKS, EKS, etc.)
- kubectl
- GitHub repository
- GitHub Container Registry (GHCR)

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

The workflows validate the Python application, build Docker images and publish them to GitHub Container Registry. Kubernetes deployment steps run when the corresponding GitHub Environment has a `KUBE_CONFIG` secret configured.

## GitHub Environment secrets

Create these GitHub Environments:

- `development`
- `production`

For each environment, add:

- `KUBE_CONFIG` = base64-encoded kubeconfig for the target cluster.

Example:

```bash
base64 -w 0 ~/.kube/config
```

Do not commit kubeconfig files, passwords or tokens.

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
- Automatic development deployment after a push to `dev` when cluster credentials are configured
- Pull-request promotion from `dev` to `main`
- Production deployment after merge when production cluster credentials are configured
- Kubernetes readiness/liveness probes and resource limits
- Environment-specific configuration

## Interview explanation

"I created a DevOps CI/CD project where the dev branch is used for development and main is protected for production. A push to dev triggers GitHub Actions, which validates the application, builds a Docker image, pushes it to GHCR and deploys it to the development Kubernetes cluster when the development environment is configured. For production, changes are promoted through a pull request from dev to main. After review and approval, merging to main triggers a separate workflow that builds the production image and deploys it to the production Kubernetes cluster. I kept dev and prod isolated using separate Kubernetes namespaces and GitHub Environments."

## Note

This is a portfolio/demo implementation. Configure your own Kubernetes cluster and GitHub Environment secrets before claiming a live cloud deployment.
