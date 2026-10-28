import sys, asyncio
from playwright.async_api import async_playwright
mode, arg = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1600, "height": 1000})
        async def shot(url, name, wait=8000, full=False):
            await pg.goto(url); await pg.wait_for_timeout(wait)
            await pg.screenshot(path=f"shots4/{name}.png", full_page=full)
        if mode == "grafana":
            pw, url315, urlns = arg.split("|", 2)
            await pg.goto("http://localhost:3000/login"); await pg.wait_for_timeout(4000)
            await pg.screenshot(path="shots4/01-grafana-login.png")
            ins = pg.locator("input"); await ins.nth(0).fill("admin"); await ins.nth(1).fill(pw)
            await pg.keyboard.press("Enter"); await pg.wait_for_timeout(5000)
            await shot("http://localhost:3000/dashboards", "02-grafana-dashboards", 5000)
            await shot("http://localhost:3000" + url315 + "?orgId=1&from=now-30m&to=now", "03-grafana-dashboard-315", 15000, True)
            await shot("http://localhost:3000" + urlns + "?orgId=1&var-namespace=default&from=now-30m&to=now", "04-grafana-namespace-pods", 15000, True)
            q = "app_http_requests_total"
            await shot("http://localhost:3000/explore?orgId=1&left=%7B%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22" + q + "%22%7D%5D,%22range%22:%7B%22from%22:%22now-15m%22,%22to%22:%22now%22%7D%7D", "05-grafana-explore-app-metric", 12000)
        elif mode == "prom":
            await shot("http://localhost:9090/targets?search=java", "06-prometheus-targets-java", 6000, True)
            await shot("http://localhost:9090/graph?g0.expr=sum(rate(container_cpu_usage_seconds_total%7Bnamespace%3D%22default%22%7D%5B5m%5D))&g0.tab=0&g0.range_input=30m", "07-prometheus-cpu-graph", 8000)
            await shot("http://localhost:9090/alerts?search=HighCPU", "08-prometheus-alert-firing", 6000, True)
        elif mode == "am":
            await shot("http://localhost:9093/#/alerts", "09-alertmanager-alert", 6000, True)
        await b.close()
asyncio.run(main())
