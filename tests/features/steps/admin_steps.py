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
        assert 'user' in orders[0]
        assert 'user_email' in orders[0]

# --- UI STEPS ---

@given('I am on the Admin Dashboard')
@when('I am on the Admin Dashboard')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/admin")
    # Wait for the dashboard to load
    context.page.wait_for_selector('h1:has-text("Admin Insights")')

@when('I go to the Products page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/products")
    context.page.wait_for_selector('.products-grid, .product-card, h1:has-text("Our Products")')

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

@when('I click on the product name "{name}" in the inventory table')
def step_impl(context, name):
    # Find the link within the inventory table that has the product name
    link = context.page.locator('.admin-table tr').filter(has_text=name).locator('a.product-cell-link')
    link.scroll_into_view_if_needed()
    link.click()

@when('I click on "Edit" for product "{name}"')
def step_impl(context, name):
    # Specifically look in the inventory table
    inventory_table = context.page.locator('#inventory-table')
    expect(inventory_table).to_be_visible(timeout=10000)
    
    # Use a more robust way to find the row: look for text anywhere in the row
    # We use filter(has_text=name) which is generally good
    try:
        row = inventory_table.locator('tr').filter(has_text=name).first
        # Ensure row exists
        expect(row).to_be_visible(timeout=5000)
        # Click the Edit button in that row - use force if needed
        row.locator('button', has_text="Edit").click(force=True)
    except Exception as e:
        context.page.screenshot(path=f"error_edit_{name.replace(' ', '_')}.png")
        # Print the table content for debugging
        print("DEBUG: Inventory Table Text:", inventory_table.inner_text())
        raise e

@when('I uncheck the "{label}" checkbox')
def step_impl(context, label):
    context.page.get_by_label(label).uncheck()

@when('I check the "{label}" checkbox')
def step_impl(context, label):
    context.page.get_by_label(label).check()

@then('the status for "{name}" should be "{status}"')
def step_impl(context, name, status):
    # Force a refresh to be sure we have latest data
    context.page.get_by_text("Refresh Stats").click()
    context.page.wait_for_timeout(3000)
    
    # Ensure we are looking at the inventory table
    table = context.page.locator('#inventory-table')
    expect(table).to_be_visible(timeout=10000)
    
    # Find the row and check badge text
    # Use a simpler filter if the full name has special characters
    search_name = name.split('(')[0].strip() if '(' in name else name
    try:
        row = table.locator('tr').filter(has_text=search_name).first
        badge = row.locator('.status-badge')
        # We expect the text to BE the status (case insensitive or exact)
        # Note: UI shows "ACTIVE" or "INACTIVE" (uppercase) based on CSS/Badge class
        expect(badge).to_contain_text(status, ignore_case=True, timeout=10000)
    except Exception as e:
        context.page.screenshot(path=f"error_status_{status}_{name.replace(' ', '_')}.png")
        print(f"DEBUG: Table text for status check: {table.inner_text()}")
        raise e

@then('I should not see product "{name}"')
def step_impl(context, name):
    # Use context.last_product_name if name matches placeholder
    actual_name = getattr(context, 'last_product_name', name) if name in ["Limited Edition Box", "Multi-Pack Saffron", "Local Image Product"] else name
    
    # Wait a bit to ensure it's filtered out
    context.page.wait_for_timeout(2000)
    
    # Check that no element with this exact text exists in the visible product cards
    # We use a locator that filters by text and ensure it's hidden or count is 0
    expect(context.page.locator('.product-card').get_by_text(actual_name)).to_have_count(0)
