import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Capture network requests
        health_request_found = False
        def handle_request(request):
            nonlocal health_request_found
            if '/health' in request.url:
                print(f"Network request found: {request.url}")
                health_request_found = True

        page.on("request", handle_request)

        print("Navigating to http://localhost:3000/...")
        await page.goto("http://localhost:3000/")

        # 1. Check if <header class="hero"> exists
        hero = page.locator("header.hero")
        if await hero.count() > 0:
            print("Found <header class='hero'>")
        else:
            print("FAILED: <header class='hero'> not found")
            await browser.close()
            sys.exit(1)

        # 2. Check if .hero-overlay exists
        overlay = page.locator(".hero-overlay")
        if await overlay.count() > 0:
            print("Found .hero-overlay")
        else:
            print("FAILED: .hero-overlay not found")

        # 3. Confirm that the hero element eventually gains the 'loaded' class
        try:
            print("Waiting for 'loaded' class on hero...")
            await page.wait_for_selector("header.hero.loaded", timeout=10000)
            print("Hero element now has 'loaded' class")
        except Exception as e:
            print(f"FAILED: Hero element did not gain 'loaded' class within 10s: {e}")

        # 4. Check for network request to /health
        # We might need to wait a bit for it to trigger as it's in onMounted
        await asyncio.sleep(2)
        if health_request_found:
            print("Backend wake-up ping (/health) detected in network requests")
        else:
            print("FAILED: Backend wake-up ping (/health) NOT detected")

        # Check CSS ::before logic
        # We can evaluate the computed style of the ::before pseudo-element
        before_style = await page.evaluate('''
            () => {
                const el = document.querySelector('header.hero');
                const before = window.getComputedStyle(el, '::before');
                return {
                    backgroundImage: before.backgroundImage,
                    opacity: before.opacity,
                    transition: before.transition
                };
            }
        ''')
        print(f"::before computed style: {before_style}")
        if 'shikara-snow-chinar-dal-lake-mountains.png' in before_style['backgroundImage']:
             print("::before has correct background image logic")
        else:
             print(f"FAILED: ::before background image mismatch: {before_style['backgroundImage']}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
