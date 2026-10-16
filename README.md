# java-redis-gitops — №1 практикалық жұмыс (ArgoCD + DevSecOps)

| Қалта | Мазмұны |
|---|---|
| `k8s/` | Java + Redis манифестері (ArgoCD бақылайды) |
| `argocd/application.yaml` | ArgoCD Application (auto-sync, prune, selfHeal) |
| `app/` | Java 17 қолданбасы, Dockerfile (multi-stage, non-root) |
| `Jenkinsfile` | Build → SonarQube → Quality Gate → Docker → Trivy → Push → GitOps update |
| `sonarqube/` | SonarQube docker-compose |
| `gatekeeper/` | `latest` tag тыйымы: ConstraintTemplate, Constraint, тест Deployment-тер |
| `scripts/run-all.sh` | Барлық қадамдарды автоматты орындау |

Іске қосу: `./scripts/run-all.sh <github-user> <dockerhub-user>`
