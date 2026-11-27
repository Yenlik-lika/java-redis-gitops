"""Pod-kill кейін подтың қалпына келу уақыты: python3 ci/recovery.py '<pods before>' <kill_ms>"""
import datetime
import json
import subprocess
import sys

before = set(sys.argv[1].split())
t_kill = int(sys.argv[2]) / 1000
pods = json.loads(subprocess.check_output(
    ["kubectl", "get", "pods", "-l", "app=java-redis-app", "-o", "json"]))["items"]
now = {p["metadata"]["name"] for p in pods}
print("Жойылған под (killed):", ", ".join(sorted(before - now)) or "-")


def ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


for p in pods:
    name = p["metadata"]["name"]
    if name in before:
        continue
    created = ts(p["metadata"]["creationTimestamp"])
    ready = [c for c in p["status"].get("conditions", []) if c["type"] == "Ready" and c["status"] == "True"]
    if ready:
        r = ts(ready[0]["lastTransitionTime"])
        print(f"Жаңа под {name}: kill-ден кейін +{created - t_kill:.0f}s құрылды, "
              f"+{r - t_kill:.0f}s Ready болды (іске қосылу -> Ready: {r - created:.0f}s)")
    else:
        print(f"Жаңа под {name}: әлі Ready емес")
