from behave import given, when, then
import requests

@given('I am logged in as admin via API')
def step_impl(context):
    payload = {
        "email": "root@thehundredvillages.com",
        "password": "root123"
    }
    response = context.api_session.post(f"{context.base_api_url}/auth/login", json=payload)
    assert response.status_code == 200
    context.token = response.json().get('token')
    context.api_session.headers.update({"Authorization": f"Bearer {context.token}"})

@given('I am logged in as admin on the UI')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/login")
    context.page.evaluate("window.localStorage.clear()")
    context.page.fill('input[type="email"]', "root@thehundredvillages.com")
    context.page.fill('input[type="password"]', "root123")
    context.page.click('button:has-text("Login")')
    
    # Wait for navigation or error
    try:
        context.page.wait_for_url(f"{context.base_ui_url}/", timeout=10000)
    except Exception as e:
        # Check if there's an error message on the page
        error_locator = context.page.locator('.error-message')
        if error_locator.is_visible():
            print(f"LOGIN FAILED: {error_locator.inner_text()}")
        context.page.screenshot(path="error_login_failed.png")
        raise e
    
    # Capture token from localStorage for any following API steps
    context.token = context.page.evaluate("window.localStorage.getItem('token')")
    if context.token:
        context.api_session.headers.update({"Authorization": f"Bearer {context.token}"})
@then('the status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code, \
        f"Expected {status_code} but got {context.response.status_code}. Response: {context.response.text}"

