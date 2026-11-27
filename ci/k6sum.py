"""k6 --summary-export JSON файлдарынан салыстыру кестесі: python3 ci/k6sum.py name=file.json ..."""
import json
import sys

rows = []
for arg in sys.argv[1:]:
    name, path = arg.split("=", 1)
    try:
        m = json.load(open(path))["metrics"]
    except Exception as e:  # noqa: BLE001
        rows.append((name, f"ERR {e}"))
        continue
    d = m["http_req_duration"]
    f = m["http_req_failed"]
    reqs = m["http_reqs"]
    rows.append((name,
                 f"reqs={reqs['count']:>7}  rps={reqs['rate']:7.1f}  "
                 f"avg={d['avg']:8.1f}ms  p95={d['p(95)']:8.1f}ms  max={d['max']:8.1f}ms  "
                 f"errors={f['value'] * 100:6.2f}%"))
for name, line in rows:
    print(f"{name:<16} {line}")
