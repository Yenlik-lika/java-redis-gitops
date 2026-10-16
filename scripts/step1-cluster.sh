#!/usr/bin/env bash
# Қадам 1: kind + kubectl орнату, кластер құру
set -e
curl -sLo /tmp/kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64 && sudo install /tmp/kind /usr/local/bin/kind
curl -sLo /tmp/kubectl "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && sudo install /tmp/kubectl /usr/local/bin/kubectl
kind create cluster --name devops
kubectl get nodes
