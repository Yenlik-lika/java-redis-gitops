#!/usr/bin/env bash
# Trivy орнату және образды сканерлеу
set -e
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin
trivy image --severity CRITICAL,HIGH java-app:v2 | tee trivy-report.txt
echo "--- Конвейер шарты (exit-code 1 = тоқтау) ---"
trivy image --exit-code 1 --severity CRITICAL --ignore-unfixed java-app:v2 && echo "PASSED" || echo "PIPELINE STOPPED: CRITICAL found"
