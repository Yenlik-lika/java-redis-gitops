#!/usr/bin/env bash
# Port-forward-тарды (қайта) іске қосу: ingress -> 8080, Prometheus -> 9090, Grafana -> 3000
pkill -f "kubectl port-forward" || true
sleep 1
setsid nohup kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80 >/dev/null 2>&1 &
if kubectl get ns monitoring >/dev/null 2>&1; then
  setsid nohup kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090 >/dev/null 2>&1 &
  setsid nohup kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80 >/dev/null 2>&1 &
fi
for i in $(seq 1 30); do
  curl -s -o /dev/null -m 2 localhost:8080/ && break
  sleep 1
done
for i in $(seq 1 30); do
  curl -s -o /dev/null -m 2 localhost:9090/-/ready && curl -s -o /dev/null -m 2 localhost:3000/api/health && break
  sleep 1
done
echo "port-forwards ready"
