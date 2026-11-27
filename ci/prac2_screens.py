"""Скриншоттар.
  python ci/prac2_screens.py rollout <out.png>
  python ci/prac2_screens.py grafana <password> '<json: [[out, expr, from_ms, to_ms], ...]>'
"""
import asyncio
import json
import sys
import urllib.parse

from playwright.async_api import async_playwright

mode = sys.argv[1]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1600, "height": 1000})
        if mode == "rollout":
            await pg.goto("http://localhost:3100/rollouts/rollout/default/java-redis-app")
            await pg.wait_for_timeout(7000)
            await pg.screenshot(path=sys.argv[2], full_page=True)
        elif mode == "grafana":
            pw = sys.argv[2]
            items = json.loads(sys.argv[3])
            await pg.goto("http://localhost:3000/login")
            await pg.wait_for_timeout(4000)
            ins = pg.locator("input")
            await ins.nth(0).fill("admin")
            await ins.nth(1).fill(pw)
            await pg.keyboard.press("Enter")
            await pg.wait_for_timeout(5000)
            for out, expr, frm, to in items:
                left = json.dumps([str(frm), str(to), "prometheus", {"refId": "A", "expr": expr}])
                await pg.goto("http://localhost:3000/explore?orgId=1&left=" + urllib.parse.quote(left))
                await pg.wait_for_timeout(9000)
                await pg.screenshot(path=out)
                print("saved", out)
        await b.close()


asyncio.run(main())
