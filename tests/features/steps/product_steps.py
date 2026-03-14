from behave import given, when, then
import requests
from playwright.sync_api import expect

# --- API STEPS ---

@when('I request categories from the API')
def step_impl(context):
    context.response = context.api_session.get(f"{context.base_api_url}/products/categories")

@then('the API should return a list of categories')
def step_impl(context):
    assert isinstance(context.response.json(), list)
    assert len(context.response.json()) > 0

@when('I search for products with keyword "{keyword}"')
def step_impl(context, keyword):
    context.response = context.api_session.get(f"{context.base_api_url}/products/?search={keyword}")

@then('the API should return products matching "{keyword}"')
def step_impl(context, keyword):
    products = context.response.json()
    assert all(keyword.lower() in p['name'].lower() for p in products)

@given('a category exists with ID {cat_id:d}')
def step_impl(context, cat_id):
    # We'll assume category 1 exists for now
    pass

import random

@when('I create a product with name "{name}", price {price:d}, and stock {stock:d}')
def step_impl(context, name, price, stock):
    unique_name = f"{name} {random.randint(1000, 9999)}"
    payload = {
        "name": unique_name,
        "price": float(price),
        "stock": stock,
        "category_id": 1
    }
    context.response = context.api_session.post(f"{context.base_api_url}/products/", json=payload)

@when('I try to create a product without an auth token')
def step_impl(context):
    # Use a fresh session without auth headers
    temp_session = requests.Session()
    payload = {"name": "Test", "price": 10.0, "category_id": 1}
    context.response = temp_session.post(f"{context.base_api_url}/products/", json=payload)

@then('the API should return an error message "{message}"')
def step_impl(context, message):
    assert context.response.json().get('message') == message

# --- UI STEPS ---

@given('I am on the Products page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/products")

@then('I should see a list of products')
def step_impl(context):
    # Wait for product cards to load
    context.page.wait_for_selector('.product-card')
    cards = context.page.locator('.product-card')
    assert cards.count() > 0

@then('I should see product "{name}"')
def step_impl(context, name):
    expect(context.page.get_by_text(name).first).to_be_visible()

@given('I am on the Admin Dashboard')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/admin")
    # Wait for the dashboard to load
    context.page.wait_for_selector('h1:has-text("Admin Insights")')

@when('I fill in the product form with name "{name}", price {price:d}, stock {stock:d}, and category ID {cat_id:d}')
def step_impl(context, name, price, stock, cat_id):
    # Open the add modal first
    context.page.click('button:has-text("+ Add New Product")')
    
    # Wait for modal content
    try:
        context.page.wait_for_selector('.modal-content', state='visible', timeout=5000)
        
        # Fill based on labels
        context.page.get_by_label("Product Name").fill(name)
        context.page.get_by_label("Price (₹)").fill(str(price))
        context.page.get_by_label("Stock").fill(str(stock))
        context.page.get_by_label("Category").select_option(str(cat_id))
    except Exception as e:
        context.page.screenshot(path="error_admin_modal.png")
        raise e

@when('I click the "{button_text}" button')
def step_impl(context, button_text):
    try:
        btn = context.page.locator(f'button:has-text("{button_text}")').first
        btn.scroll_into_view_if_needed(timeout=5000)
        btn.click(force=True, timeout=5000)
    except Exception as e:
        context.page.screenshot(path=f"error_click_{button_text.replace(' ', '_')}.png")
        raise e

@then('I should see the product "{name}" in the product list')
def step_impl(context, name):
    # Check the specific admin table
    expect(context.page.locator('table.admin-table')).to_contain_text(name)
