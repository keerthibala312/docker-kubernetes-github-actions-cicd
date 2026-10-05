# GitHub branch protection checklist

## main
- Require a pull request before merging
- Require at least 1 approval
- Require status checks to pass where appropriate
- Restrict direct pushes

## dev
- Allow normal development pushes
- Trigger the development workflow on push

## GitHub Environments
Create:
- development
- production

The workflows create an ephemeral Kind Kubernetes cluster inside the GitHub Actions runner, so a kubeconfig secret is not required for this demo.

For a real cloud deployment, replace the Kind setup with AKS, EKS, GKE, or another reachable cluster and store the required credentials as GitHub Environment secrets.

Do not commit kubeconfig files, passwords or tokens.
