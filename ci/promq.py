"""PromQL сұрауы: python3 ci/promq.py '<query>' [--value]"""
import json
import sys
import urllib.parse
import urllib.request

q = sys.argv[1]
only_value = "--value" in sys.argv
url = "http://localhost:9090/api/v1/query?" + urllib.parse.urlencode({"query": q})
try:
    res = json.load(urllib.request.urlopen(url, timeout=10))["data"]["result"]
except Exception as e:  # noqa: BLE001
    print("nan" if only_value else f"ERR {e}")
    sys.exit(0)
if only_value:
    print(res[0]["value"][1] if res else "nan")
else:
    print(f"PromQL: {q}")
    for r in res:
        print(" ", json.dumps(r["metric"], ensure_ascii=False), "=", r["value"][1])
    if not res:
        print("  (empty)")
