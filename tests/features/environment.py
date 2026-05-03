from playwright.sync_api import sync_playwright
import requests
import os

# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================
# Control which environment the test suite targets using:
#
#   $env:TEST_ENV = "local"    → localhost:5000 / localhost:3000  (default)
#   $env:TEST_ENV = "staging"  → THV-test on Render / Vercel preview
#   $env:TEST_ENV = "prod"     → THV-1 on Render / kashmiri-heritage on Vercel
#
# Or override directly:
#   $env:API_URL = "https://thv-1.onrender.com/api"
#   $env:UI_URL  = "https://kashmiri-heritage.vercel.app"
#
# ============================================================

ENVIRONMENTS = {
    "local": {
        "api": "http://localhost:5000/api",
        "ui": "http://localhost:3000",
    },
    "staging": {
        "api": os.environ.get("STAGING_API_URL", "https://thv-test.onrender.com/api"),
        "ui":  os.environ.get("STAGING_UI_URL",  "https://thv-test.vercel.app"),
    },
    "prod": {
        "api": os.environ.get("PROD_API_URL", "https://thv-1.onrender.com/api"),
        "ui":  os.environ.get("PROD_UI_URL",  "https://kashmiri-heritage.vercel.app"),
    },
}

def _resolve_urls():
    """Return (api_url, ui_url) based on env vars."""
    # Allow full manual override
    if os.environ.get("API_URL"):
        api = os.environ["API_URL"].rstrip("/")
        ui  = os.environ.get("UI_URL", "http://localhost:3000").rstrip("/")
        return api, ui

    env_name = os.environ.get("TEST_ENV", "local").lower()
    env = ENVIRONMENTS.get(env_name, ENVIRONMENTS["local"])
    return env["api"].rstrip("/"), env["ui"].rstrip("/")


def before_all(context):
    # Setup Playwright for UI tests
    context.playwright = sync_playwright().start()
    is_headless = os.environ.get('HEADLESS', 'true').lower() == 'true'
    context.browser = context.playwright.chromium.launch(headless=is_headless)

    # ---- Resolve base URLs from environment ----
    context.base_api_url, context.base_ui_url = _resolve_urls()
    print(f"\n[TEST CONFIG] API  → {context.base_api_url}")
    print(f"[TEST CONFIG] UI   → {context.base_ui_url}")
    print(f"[TEST CONFIG] ENV  → {os.environ.get('TEST_ENV', 'local')}\n")

    # Session for API tests
    context.api_session = requests.Session()


def after_all(context):
    context.browser.close()
    context.playwright.stop()


def before_scenario(context, scenario):
    # Reset product state via API before each scenario to ensure visibility and stock
    # Only do this for local/staging (skip for prod to avoid touching live data)
    env_name = os.environ.get("TEST_ENV", "local").lower()
    if env_name != "prod":
        try:
            login_res = requests.post(f"{context.base_api_url}/auth/login", json={
                "email": "root@thehundredvillages.com",
                "password": "root123"
            })
            if login_res.status_code == 200:
                token = login_res.json().get('token')
                prods_res = requests.get(
                    f"{context.base_api_url}/products/?admin=true",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if prods_res.status_code == 200:
                    products = prods_res.json()
                    for p in products:
                        if not p.get('is_active') or p.get('stock', 0) < 10:
                            requests.put(
                                f"{context.base_api_url}/products/{p['id']}",
                                json={"is_active": True, "stock": 100},
                                headers={"Authorization": f"Bearer {token}"}
                            )
        except Exception as e:
            print(f"WARNING: Failed to reset product state: {e}")

    # Create a fresh browser context for each UI scenario
    if "ui" in scenario.tags:
        context.browser_context = context.browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        context.browser_context.set_default_timeout(60000)
        context.page = context.browser_context.new_page()
        context.page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))


def after_scenario(context, scenario):
    if "ui" in scenario.tags:
        context.page.close()
        context.browser_context.close()
