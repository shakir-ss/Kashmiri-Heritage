from behave import given, when, then
import requests
from playwright.sync_api import expect

# --- API STEPS ---

@given('the API is accessible')
def step_impl(context):
    # Health check is at root /health, not /api/health
    url = context.base_api_url.replace('/api', '') + "/health"
    response = context.api_session.get(url)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. URL: {url}"

@when('I register a new user with name "{name}", email "{email}", and password "{password}"')
def step_impl(context, name, email, password):
    payload = {
        "name": name,
        "email": email,
        "password": password
    }
    context.response = context.api_session.post(f"{context.base_api_url}/auth/register", json=payload)

@then('the API should return a success message "{message}"')
def step_impl(context, message):
    assert context.response.json().get('message') == message

@then('the status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code

@given('I have a registered user with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    # This assumes the user already exists (like our root admin)
    pass

@when('I login via API with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    payload = {
        "email": email,
        "password": password
    }
    context.response = context.api_session.post(f"{context.base_api_url}/auth/login", json=payload)

@then('the API should return a JWT token')
def step_impl(context):
    assert 'token' in context.response.json()

# --- UI STEPS ---

@given('I am on the Login page')
def step_impl(context):
    print(f"Navigating to {context.base_ui_url}/login")
    # Go to a neutral page first or just clear after first navigation
    context.page.goto(context.base_ui_url)
    context.page.evaluate("window.localStorage.clear()")
    context.page.goto(f"{context.base_ui_url}/login")
    # Take a screenshot for debugging
    context.page.screenshot(path="debug_login_page.png")

@when('I enter email "{email}" and password "{password}"')
def step_impl(context, email, password):
    try:
        context.page.wait_for_selector('input[type="email"]', timeout=5000)
        context.page.fill('input[type="email"]', email)
        context.page.fill('input[type="password"]', password)
    except Exception as e:
        context.page.screenshot(path="debug_fill_error.png")
        raise e

@when('I click the login button')
def step_impl(context):
    # We'll use a locator for the login button, assuming it has a recognizable text or selector
    context.page.click('button:has-text("Login")')

@then('I should be redirected to the Home page')
def step_impl(context):
    # Wait for the URL to change to the home page (root or /)
    context.page.wait_for_url(f"{context.base_ui_url}/")
    expect(context.page).to_have_url(f"{context.base_ui_url}/")

@then('I should see a logout option')
def step_impl(context):
    # Assuming there's a logout button/link visible when logged in
    expect(context.page.get_by_text("Logout")).to_be_visible()
