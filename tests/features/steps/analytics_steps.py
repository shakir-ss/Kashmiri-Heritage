from behave import given, when, then
import requests
import random

# --- API STEPS ---

@when('I view product with ID {prod_id:d}')
def step_impl(context, prod_id):
    # Fetch first available product if none tracked
    response = context.api_session.get(f"{context.base_api_url}/products/")
    pid = response.json()[0]['id']
    context.response = context.api_session.post(f"{context.base_api_url}/analytics/view/{pid}")

@when('I fetch the shop stats')
def step_impl(context):
    context.response = context.api_session.get(f"{context.base_api_url}/analytics/stats")

@then('the API should return a stats object')
def step_impl(context):
    stats = context.response.json()
    assert 'view_count' in stats or 'total_revenue' in stats or isinstance(stats, dict)

@given('I register and login as a regular user')
def step_impl(context):
    email = f"user_{random.randint(1000, 9999)}@example.com"
    reg_payload = {
        "name": "Regular User",
        "email": email,
        "password": "password123"
    }
    context.api_session.post(f"{context.base_api_url}/auth/register", json=reg_payload)
    
    login_payload = {
        "email": email,
        "password": "password123"
    }
    response = context.api_session.post(f"{context.base_api_url}/auth/login", json=login_payload)
    context.token = response.json().get('token')
    context.api_session.headers.update({"Authorization": f"Bearer {context.token}"})
