from playwright.sync_api import sync_playwright
import requests

def before_all(context):
    # Setup Playwright for UI tests
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)
    
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
    # Create a fresh browser context for each UI scenario
    if "ui" in scenario.tags:
        context.browser_context = context.browser.new_context()
        context.page = context.browser_context.new_page()

def after_scenario(context, scenario):
    # Close browser context after each UI scenario
    if "ui" in scenario.tags:
        context.page.close()
        context.browser_context.close()
