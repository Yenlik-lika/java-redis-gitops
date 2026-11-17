import sys, json, urllib.request, urllib.parse, time
# Usage: logql.py "<query>" [minutes_back|start_ns:end_ns] [limit]
q = sys.argv[1]; rng = sys.argv[2] if len(sys.argv) > 2 else "30"; limit = sys.argv[3] if len(sys.argv) > 3 else "15"
if ":" in rng:
    start, end = rng.split(":")
else:
    end = str(time.time_ns()); start = str(time.time_ns() - int(rng) * 60 * 10**9)
url = "http://localhost:3100/loki/api/v1/query_range?" + urllib.parse.urlencode(
    {"query": q, "start": start, "end": end, "limit": limit, "direction": "backward", "step": "60"})
d = json.load(urllib.request.urlopen(url))
res = d.get("data", {}).get("result", [])
print(f"LogQL> {q}")
if d.get("data", {}).get("resultType") == "matrix":
    for s in res:
        print("  series", s["metric"])
        for ts, v in s["values"][-10:]:
            print("   ", time.strftime("%H:%M:%S", time.gmtime(int(float(ts)))), "->", v)
else:
    n = 0
    for s in res:
        lbl = {k: s["stream"].get(k) for k in ("namespace", "app", "pod", "container", "level", "status") if s["stream"].get(k)}
        print("  stream", lbl)
        for ts, line in s["values"]:
            n += 1
            print("   ", line[:220])
    print(f"  => {n} lines")
print()
