#!/usr/bin/env bash
# Vault ішінде: құпияны сақтау, Kubernetes auth, policy және role баптау
set -e
V="kubectl exec vault-0 --"

# 2-қадам: статус және root токенмен кіру (dev режимде root токен = "root")
$V vault status
$V vault login root

# 3-қадам: Redis құпиясөзін Vault-та сақтау (KV v2, secret/ жолы)
$V vault kv put secret/redis-app password="MySecretPass123"
$V vault kv get secret/redis-app

# Kubernetes auth: подтар өз ServiceAccount токенімен Vault-қа кіре алуы үшін
$V vault auth enable kubernetes || true
$V sh -c 'vault write auth/kubernetes/config kubernetes_host="https://${KUBERNETES_PORT_443_TCP_ADDR}:443"'

# 7-қадам: policy — тек оқу құқығы
kubectl exec -i vault-0 -- vault policy write app-policy - < vault/app-policy.hcl
$V vault policy read app-policy

# app-role: тек java-app және redis ServiceAccount-тары (default namespace) осы рөлді ала алады
$V vault write auth/kubernetes/role/app-role \
    bound_service_account_names=java-app,redis \
    bound_service_account_namespaces=default \
    policies=app-policy \
    ttl=1h
$V vault read auth/kubernetes/role/app-role
