# №2 практикалық жұмыс: ортақ bash функциялары (source ci/prac2_lib.sh)

# Rollout фазасын күту: waitphase Paused|Healthy|Degraded [max_tries]
waitphase() {
  for i in $(seq 1 "${2:-60}"); do
    p=$(kubectl get rollout java-redis-app -o jsonpath='{.status.phase}' 2>/dev/null)
    echo "  [$i] rollout phase=$p"
    [ "$p" = "$1" ] && return 0
    sleep 5
  done
  return 1
}

# Ingress арқылы N сұрау, жауап нұсқалары бойынша санау (v1/v2/v3-bug)
versions() {
  for i in $(seq 1 "$1"); do (curl -s -m 5 localhost:8080/ || true) | awk '{print $2}'; echo; done | (grep -v '^$' || true) | sort | uniq -c
}

# Ingress арқылы N сұрау, HTTP кодтары бойынша санау
codes() {
  for i in $(seq 1 "$1"); do curl -s -m 5 -o /dev/null -w '%{http_code}\n' localhost:8080/ || true; done | sort | uniq -c
}

canary_weight() {
  kubectl get ingress -o yaml | grep canary-weight || echo "  (canary ingress жоқ)"
}

now_ms() { date +%s%3N; }
