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

Add a separate KUBE_CONFIG secret to each environment.
Use required reviewers on the production environment if an approval gate is desired.

Do not commit kubeconfig files, passwords or tokens.
