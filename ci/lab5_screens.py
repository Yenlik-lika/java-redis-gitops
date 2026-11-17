import sys, json, asyncio, urllib.parse
from playwright.async_api import async_playwright
pw = sys.argv[1]; t_from = sys.argv[2]; t_to = sys.argv[3]
def explore(expr, frm="now-30m", to="now"):
    left = json.dumps([frm, to, "Loki", {"refId": "A", "expr": expr}])
    return "http://localhost:3000/explore?orgId=1&left=" + urllib.parse.quote(left)
Q = {
 "04-explore-all-logs": '{namespace="default", app="java-redis-app"}',
 "05-explore-error-text": '{namespace="default", app="java-redis-app"} |= "level=ERROR"',
 "06-explore-level-logfmt": '{namespace="default", app="java-redis-app"} | logfmt | level="ERROR"',
 "07-explore-status-500": '{namespace="default", app="java-redis-app"} | logfmt | status="500"',
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1600, "height": 1000})
        await pg.goto("http://localhost:3000/login"); await pg.wait_for_timeout(4000)
        await pg.screenshot(path="shots5/01-grafana-login.png")
        ins = pg.locator("input"); await ins.nth(0).fill("admin"); await ins.nth(1).fill(pw)
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(5000)
        await pg.goto("http://localhost:3000/datasources"); await pg.wait_for_timeout(4000)
        await pg.screenshot(path="shots5/02-datasources.png")
        await pg.goto("http://localhost:3000/datasources"); await pg.wait_for_timeout(2000)
        try:
            await pg.get_by_text("Loki", exact=True).first.click(); await pg.wait_for_timeout(3000)
            btn = pg.get_by_role("button", name="Save & test")
            if await btn.count(): await btn.first.click(); await pg.wait_for_timeout(5000)
            await pg.screenshot(path="shots5/03-loki-datasource-test.png", full_page=True)
        except Exception as e:
            print("ds page:", e)
        for name, q in Q.items():
            await pg.goto(explore(q)); await pg.wait_for_timeout(9000)
            await pg.screenshot(path=f"shots5/{name}.png")
        await pg.goto(explore('{namespace="default", app="java-redis-app"} |= "level=ERROR"', t_from, t_to)); await pg.wait_for_timeout(9000)
        await pg.screenshot(path="shots5/08-explore-time-range.png")
        await pg.goto(explore('sum(count_over_time({namespace="default", app="java-redis-app"} |= "level=ERROR" [1m]))')); await pg.wait_for_timeout(9000)
        await pg.screenshot(path="shots5/09-explore-error-count.png")
        await pg.goto("http://localhost:3000/d/java-app-errors/?orgId=1&from=now-30m&to=now"); await pg.wait_for_timeout(12000)
        await pg.screenshot(path="shots5/10-dashboard-errors.png", full_page=True)
        await b.close()
asyncio.run(main())
