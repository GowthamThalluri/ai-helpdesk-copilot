#!/usr/bin/env bash

set -Eeuo pipefail

# --------------------------------------------------
# Helpdesk Copilot - Local Kubernetes Deployment
# --------------------------------------------------

NAMESPACE="helpdesk"
KUBE_CONTEXT="${KUBE_CONTEXT:-helpdesk-local}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

SECRET_FILE="$REPO_ROOT/k8s/secret.env"

log() {
    printf '\n==> %s\n' "$1"
}

die() {
    printf '\nERROR: %s\n' "$1" >&2
    exit 1
}

run_kubectl() {
    kubectl --context="$KUBE_CONTEXT" "$@"
}

# --------------------------------------------------
# 1. Check required tools and files
# --------------------------------------------------

log "Checking prerequisites"

command -v kubectl >/dev/null 2>&1 \
    || die "kubectl is not installed or not available in PATH."

[[ -f "$SECRET_FILE" ]] \
    || die "Local Secret file not found: k8s/secret.env"

for manifest in \
    namespace.yaml \
    configmap.yaml \
    postgres-pvc.yaml \
    postgres-service.yaml \
    postgres-statefulset.yaml \
    fastapi-service.yaml \
    fastapi-deployment.yaml
do
    [[ -f "$REPO_ROOT/k8s/$manifest" ]] \
        || die "Required manifest is missing: k8s/$manifest"
done

grep -Eq '^POSTGRES_USER=.+$' "$SECRET_FILE" \
    || die "POSTGRES_USER is missing or empty in k8s/secret.env"

grep -Eq '^POSTGRES_PASSWORD=.+$' "$SECRET_FILE" \
    || die "POSTGRES_PASSWORD is missing or empty in k8s/secret.env"

log "Checking Kubernetes connection"

run_kubectl cluster-info >/dev/null 2>&1 \
    || die "Cannot connect to context '$KUBE_CONTEXT'. Start Minikube with: minikube start -p helpdesk-local"

cd "$REPO_ROOT"

# --------------------------------------------------
# 2. Create namespace
# --------------------------------------------------

log "Applying namespace"

run_kubectl apply -f k8s/namespace.yaml

# --------------------------------------------------
# 3. Apply application configuration
# --------------------------------------------------

log "Applying ConfigMap"

run_kubectl apply -f k8s/configmap.yaml

# --------------------------------------------------
# 4. Create or update Secret securely
# --------------------------------------------------

log "Creating or updating PostgreSQL Secret"

run_kubectl create secret generic helpdesk-db-secret \
    --namespace="$NAMESPACE" \
    --from-env-file="$SECRET_FILE" \
    --dry-run=client \
    -o yaml |
    run_kubectl apply -f -

# --------------------------------------------------
# 5. Apply persistent storage
# --------------------------------------------------

log "Applying PostgreSQL PVC"

run_kubectl apply -f k8s/postgres-pvc.yaml

log "Waiting for PostgreSQL PVC to become Bound"

run_kubectl wait \
    --for=jsonpath='{.status.phase}'=Bound \
    pvc/postgres-data \
    --namespace="$NAMESPACE" \
    --timeout=120s

# --------------------------------------------------
# 6. Deploy PostgreSQL
# --------------------------------------------------

log "Applying PostgreSQL Services"

run_kubectl apply -f k8s/postgres-service.yaml

log "Applying PostgreSQL StatefulSet"

run_kubectl apply -f k8s/postgres-statefulset.yaml

log "Waiting for PostgreSQL StatefulSet"

run_kubectl rollout status \
    statefulset/postgres \
    --namespace="$NAMESPACE" \
    --timeout=180s

# --------------------------------------------------
# 7. Deploy FastAPI
# --------------------------------------------------

log "Applying FastAPI Service"

run_kubectl apply -f k8s/fastapi-service.yaml

log "Applying FastAPI Deployment"

run_kubectl apply -f k8s/fastapi-deployment.yaml

log "Waiting for FastAPI Deployment"

run_kubectl rollout status \
    deployment/helpdesk-api \
    --namespace="$NAMESPACE" \
    --timeout=180s

# --------------------------------------------------
# 8. Verify application health
# --------------------------------------------------

log "Checking application health and database readiness"

run_kubectl exec \
    deployment/helpdesk-api \
    --namespace="$NAMESPACE" \
    -- python -c '
import urllib.request

for path in ("/health", "/ready"):
    with urllib.request.urlopen(
        "http://127.0.0.1:8000" + path,
        timeout=5
    ) as response:
        print(
            f"{path}: HTTP {response.status} "
            f"{response.read().decode()}"
        )
'

# --------------------------------------------------
# 9. Display final resource status
# --------------------------------------------------

log "Final Kubernetes resource status"

run_kubectl get pods,services,pvc --namespace="$NAMESPACE"

log "Deployment completed successfully"
