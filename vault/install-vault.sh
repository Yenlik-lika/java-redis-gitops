#!/usr/bin/env bash
# 1-қадам: Vault-ты Helm арқылы dev-режимде орнату (Agent Injector әдепкіде қосулы)
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm install vault hashicorp/vault --set "server.dev.enabled=true"
