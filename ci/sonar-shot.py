import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1600,"height":900})
        await pg.goto("http://localhost:9000/sessions/new"); await pg.wait_for_timeout(3000)
        await pg.fill("input[name=login]", "admin"); await pg.fill("input[name=password]", "Admin12345!x")
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(5000)
        await pg.goto("http://localhost:9000/dashboard?id=java-app"); await pg.wait_for_timeout(8000)
        await pg.screenshot(path="shots/07-sonarqube.png", full_page=True); await b.close()
asyncio.run(main())
