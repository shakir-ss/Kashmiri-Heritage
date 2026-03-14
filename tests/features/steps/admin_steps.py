from behave import given, when, then
import requests
from playwright.sync_api import expect

# --- API STEPS ---

@when('I request the admin order list')
def step_impl(context):
    context.response = context.api_session.get(f"{context.base_api_url}/orders/admin")

@then('the API should return a list of all customer orders')
def step_impl(context):
    orders = context.response.json()
    assert isinstance(orders, list)
    if len(orders) > 0:
        # Check for admin-specific fields
        assert 'customer_name' in orders[0]
        assert 'customer_email' in orders[0]

# --- UI STEPS ---

@given('I am on the Admin Dashboard')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/admin")
    # Wait for the dashboard to load
    context.page.wait_for_selector('h1:has-text("Admin Insights")')

@then('I should see the "{title}" table')
def step_impl(context, title):
    expect(context.page.get_by_text(title)).to_be_visible()

@then('the table should contain at least one order')
def step_impl(context):
    # Wait for the table to potentially load
    context.page.wait_for_timeout(2000)
    
    # Select rows in the orders table
    rows = context.page.locator('section:has-text("Recent Customer Orders") table tbody tr')
    
    # If the first row says "No orders placed yet", let's wait a bit more or check again
    # In a real app, we might trigger a refresh if the test requires data
    
    row_count = rows.count()
    if row_count == 1:
        text = rows.first.inner_text()
        if "No orders placed yet" in text:
            # Maybe place an order via API real quick to ensure data exists if needed?
            # For now, let's just assert and we know smoke test above placed one.
            # But the UI might need a refresh.
            context.page.click('button:has-text("Refresh Stats")')
            context.page.wait_for_timeout(2000)
            rows = context.page.locator('section:has-text("Recent Customer Orders") table tbody tr')

    first_row_text = rows.first.inner_text()
    assert "No orders placed yet" not in first_row_text, f"Expected orders but found: {first_row_text}"

