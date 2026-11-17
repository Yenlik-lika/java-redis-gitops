#!/usr/bin/env bash
# 1-қадам: Loki стекін орнату (Loki + Promtail + Grafana)
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install loki grafana/loki-stack -n logging --create-namespace \
  --set grafana.enabled=true,promtail.enabled=true
