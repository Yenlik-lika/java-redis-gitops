#!/usr/bin/env bash
# OPA Gatekeeper: latest tag тыйымы
set -e
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/v3.17.1/deploy/gatekeeper.yaml
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-controller-manager --timeout=300s
kubectl apply -f gatekeeper/template-disallow-latest.yaml; sleep 15
kubectl apply -f gatekeeper/constraint-disallow-latest.yaml; sleep 15
echo "=== nginx:latest (тыйым салынуы керек) ==="
kubectl apply -f gatekeeper/bad-deployment.yaml || true
echo "=== nginx:1.27 (рұқсат етілуі керек) ==="
kubectl apply -f gatekeeper/good-deployment.yaml
