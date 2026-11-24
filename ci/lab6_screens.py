import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1500, "height": 950})
        async def shot(name, full=False):
            await pg.screenshot(path=f"shots6/{name}.png", full_page=full)
        await pg.goto("http://localhost:8200/ui/vault/auth?with=token"); await pg.wait_for_timeout(5000)
        await shot("01-vault-login")
        try:
            box = pg.locator("input[name=token], input[type=password]").first
            await box.fill("root"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(5000)
        except Exception as e:
            print("login:", e)
        await shot("02-vault-dashboard")
        for name, urls in [
            ("03-secret-engines", ["http://localhost:8200/ui/vault/secrets"]),
            ("04-secret-redis-app", ["http://localhost:8200/ui/vault/secrets/secret/kv/redis-app/details",
                                     "http://localhost:8200/ui/vault/secrets/secret/show/redis-app"]),
            ("06-policy-app-policy", ["http://localhost:8200/ui/vault/policy/acl/app-policy"]),
            ("07-auth-methods", ["http://localhost:8200/ui/vault/access"]),
        ]:
            for u in urls:
                await pg.goto(u); await pg.wait_for_timeout(5000)
                if "not found" not in (await pg.content()).lower(): break
            await shot(name)
            if name == "04-secret-redis-app":
                try:
                    eye = pg.locator("button[aria-label*='show' i], button:has-text('Reveal'), [data-test-masked-input] button").first
                    await eye.click(); await pg.wait_for_timeout(1500)
                except Exception as e:
                    print("reveal:", e)
                await shot("05-secret-redis-app-revealed")
        await b.close()
asyncio.run(main())
