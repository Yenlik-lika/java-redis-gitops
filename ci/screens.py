import sys, asyncio
from playwright.async_api import async_playwright
pw_ = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(ignore_https_errors=True, viewport={"width":1600,"height":900})
        await pg.goto("https://localhost:8080/login"); await pg.wait_for_timeout(4000)
        await pg.screenshot(path="shots/02-argocd-login.png")
        ins = pg.locator("input"); await ins.nth(0).fill("admin"); await ins.nth(1).fill(pw_)
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(6000)
        await pg.screenshot(path="shots/03a-argocd-apps.png")
        await pg.goto("https://localhost:8080/applications/argocd/java-redis-app"); await pg.wait_for_timeout(8000)
        await pg.screenshot(path="shots/03b-argocd-tree.png")
        await pg.goto("https://localhost:8080/applications/argocd/java-redis-app?resource=&node=&tab=history"); await pg.wait_for_timeout(3000)
        await pg.goto("https://localhost:8080/applications/argocd/java-redis-app?rollback=0"); await pg.wait_for_timeout(5000)
        await pg.screenshot(path="shots/04-argocd-history.png")
        await b.close()
asyncio.run(main())
