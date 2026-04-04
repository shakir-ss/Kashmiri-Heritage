from playwright.sync_api import sync_playwright
import requests

import os

def before_all(context):
    # Setup Playwright for UI tests
    context.playwright = sync_playwright().start()
    is_headless = os.environ.get('HEADLESS', 'true').lower() == 'true'
    context.browser = context.playwright.chromium.launch(headless=is_headless)
    
    # Base URLs
    context.base_api_url = "http://localhost:5000/api"
    context.base_ui_url = "http://localhost:3000"
    
    # Session for API tests
    context.api_session = requests.Session()

def after_all(context):
    # Teardown Playwright
    context.browser.close()
    context.playwright.stop()

def before_scenario(context, scenario):
    # Reset product state via API before each scenario to ensure visibility and stock
    try:
        login_res = requests.post("http://localhost:5000/api/auth/login", json={
            "email": "root@thehundredvillages.com",
            "password": "root123"
        })
        if login_res.status_code == 200:
            token = login_res.json().get('token')
            # Fetch all products (including inactive ones)
            prods_res = requests.get("http://localhost:5000/api/products/?admin=true", headers={"Authorization": f"Bearer {token}"})
            if prods_res.status_code == 200:
                products = prods_res.json()
                for p in products:
                    # If product is inactive or low on stock, reset it
                    if not p.get('is_active') or p.get('stock', 0) < 10:
                        requests.put(f"http://localhost:5000/api/products/{p['id']}", 
                                   json={"is_active": True, "stock": 100}, 
                                   headers={"Authorization": f"Bearer {token}"})
    except Exception as e:
        print(f"WARNING: Failed to reset product state: {e}")

    # Create a fresh browser context for each UI scenario
    if "ui" in scenario.tags:
        # Setup context with a standard desktop viewport
        context.browser_context = context.browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        # Increase default timeout to 60s
        context.browser_context.set_default_timeout(60000)
        context.page = context.browser_context.new_page()
        # Enable console logging
        context.page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

def after_scenario(context, scenario):
    # Close browser context after each UI scenario
    if "ui" in scenario.tags:
        context.page.close()
        context.browser_context.close()
