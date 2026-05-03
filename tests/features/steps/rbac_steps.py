"""
rbac_steps.py — Steps for: role_permissions.feature
Updated to use dynamic base_api_url from environment.py
"""
from behave import given, when, then
import requests
from playwright.sync_api import expect

ADMIN_EMAIL = "root@thehundredvillages.com"
ADMIN_PASS = "root123"
SUBADMIN_EMAIL = "subadmin@thehundredvillages.com"
SUBADMIN_PASS = "subadmin123"

# ============================================================
# ROLE PERMISSION STEPS
# ============================================================

@given('I am logged in as sub-admin via API')
def step_impl(context):
    """Login as sub-admin. Create the account via admin if it doesn't exist."""
    login_res = requests.post(f"{context.base_api_url}/auth/login", json={
        "email": SUBADMIN_EMAIL, "password": SUBADMIN_PASS
    })
    if login_res.status_code != 200:
        admin_login = requests.post(f"{context.base_api_url}/auth/login", json={
            "email": ADMIN_EMAIL, "password": ADMIN_PASS
        })
        admin_token = admin_login.json()['token']
        requests.post(f"{context.base_api_url}/auth/register", json={
            "name": "Sub Admin",
            "email": SUBADMIN_EMAIL,
            "password": SUBADMIN_PASS,
            "role": "sub-admin"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        login_res = requests.post(f"{context.base_api_url}/auth/login", json={
            "email": SUBADMIN_EMAIL, "password": SUBADMIN_PASS
        })
    token = login_res.json()['token']
    context.api_session.headers.update({"Authorization": f"Bearer {token}"})

@given('I am logged in as sub-admin on the UI')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/login")
    context.page.wait_for_selector('input[type="email"]', state='visible')
    context.page.fill('input[type="email"]', SUBADMIN_EMAIL)
    context.page.fill('input[type="password"]', SUBADMIN_PASS)
    context.page.locator('button[type="submit"], button:has-text("Login")').first.click()
    context.page.wait_for_url(f"{context.base_ui_url}/", timeout=10000)
    context.page.wait_for_timeout(2000)

@given('a test product "{name}" exists')
def step_impl(context, name):
    """Create a throwaway product for delete testing."""
    res = context.api_session.post(f"{context.base_api_url}/products/", json={
        "name": name,
        "price": 99,
        "stock": 5,
        "category_id": 1,
        "description": "Temp test product"
    })
    assert res.status_code == 201, f"Failed to create test product: {res.text}"
    data = res.json()
    context.test_product_id = data.get('product_id') or data.get('id')

@when('I delete the test product via API')
def step_impl(context):
    context.response = context.api_session.delete(
        f"{context.base_api_url}/products/{context.test_product_id}"
    )

@when('I try to delete product {product_id:d} via API')
def step_impl(context, product_id):
    context.response = context.api_session.delete(f"{context.base_api_url}/products/{product_id}")

@when('I try to update the price of product {product_id:d} to {new_price:d} via API')
def step_impl(context, product_id, new_price):
    context.response = context.api_session.put(
        f"{context.base_api_url}/products/{product_id}",
        json={"price": new_price}
    )

@then('I should not see any "Delete" buttons on the Products table')
def step_impl(context):
    delete_buttons = context.page.locator('.admin-table button', has_text='Delete')
    count = delete_buttons.count()
    assert count == 0, f"Expected no Delete buttons for sub-admin, but found {count}"

@then('I should not see the Revenue analytics cards')
def step_impl(context):
    revenue_card = context.page.locator('.stat-card', has_text='Revenue')
    count = revenue_card.count()
    assert count == 0, f"Revenue card should be hidden for sub-admin, found {count}"

@then('I should see "Delete" buttons on the Products table')
def step_impl(context):
    delete_buttons = context.page.locator('.admin-table button', has_text='Delete')
    expect(delete_buttons.first).to_be_visible(timeout=8000)

@then('I should see the Revenue analytics cards')
def step_impl(context):
    revenue_card = context.page.locator('.stat-card', has_text='Revenue').first
    expect(revenue_card).to_be_visible(timeout=8000)

@then('the API should return an error message containing "{text}"')
def step_impl(context, text):
    data = context.response.json()
    msg = data.get('message', '') or data.get('error', '') or str(data)
    assert text.lower() in msg.lower(), \
        f"Expected '{text}' in error message, got: '{msg}'"

# NOTE: The following steps are defined in existing step files and must NOT be re-defined here:
#   @given('I register and login as a regular user')  -> analytics_steps.py:23
#   @when('I request the admin order list')           -> admin_steps.py:7
#   @given('I am logged in as admin via API')         -> common_steps.py:4
#   @then('the status code should be {code:d}')       -> common_steps.py:38
