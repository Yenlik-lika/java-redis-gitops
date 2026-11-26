import asyncio, os
from playwright.async_api import async_playwright

BASE = "http://localhost:8200"
TOKEN = os.environ.get("VAULT_UI_TOKEN", "root")


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1500, "height": 950})
        pg = await ctx.new_page()

        async def shot(name):
            await pg.screenshot(path=f"shots6/{name}.png")

        async def text():
            try:
                return (await pg.inner_text("body")).lower()
            except Exception:
                return ""

        async def open_first_ok(urls, must):
            """open the first URL whose page text contains `must`"""
            for u in urls:
                await pg.goto(BASE + u)
                await pg.wait_for_timeout(4500)
                t = await text()
                print("TRY", u, "->", pg.url, "| ok" if must in t else "| miss")
                if must in t and "sign in to vault" not in t:
                    return True
            return False

        await pg.goto(BASE + "/ui/vault/auth?with=token")
        await pg.wait_for_timeout(4000)
        await shot("01-vault-login")
        box = pg.locator("input[name=token], input[type=password]").first
        await box.fill(TOKEN)
        await pg.keyboard.press("Enter")
        await pg.wait_for_timeout(5000)
        await shot("02-vault-dashboard")
        print("after login:", pg.url)

        # a non-root token is kept in the browser session, so page.goto() keeps us logged in
        await open_first_ok(["/ui/vault/secrets-engines", "/ui/vault/secrets"], "secret")
        await shot("03-secret-engines")

        ok = await open_first_ok([
            "/ui/vault/secrets-engines/secret/kv/redis-app",
            "/ui/vault/secrets-engines/secret/kv/redis-app/details",
            "/ui/vault/secrets/secret/kv/redis-app",
            "/ui/vault/secrets/secret/kv/redis-app/details",
            "/ui/vault/secrets/secret/show/redis-app",
        ], "redis-app")
        await shot("04-secret-redis-app")
        if ok:
            try:
                eye = pg.locator(
                    "button[aria-label*='show' i], button[aria-label*='reveal' i], "
                    "button:has-text('Reveal'), button:has-text('Show'), "
                    "[data-test-masked-input] button, [data-test-button='toggle-masked']"
                ).first
                await eye.click()
                await pg.wait_for_timeout(1500)
            except Exception as e:
                print("reveal:", e)
        await shot("05-secret-redis-app-revealed")

        await open_first_ok(["/ui/vault/policy/acl/app-policy",
                             "/ui/vault/policy/acl/app-policy/edit"], "app-policy")
        await shot("06-policy-app-policy")

        await open_first_ok(["/ui/vault/access", "/ui/vault/access/methods"], "kubernetes")
        await shot("07-auth-methods")
        await b.close()

asyncio.run(main())
