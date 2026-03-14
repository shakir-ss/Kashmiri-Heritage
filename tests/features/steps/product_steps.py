from behave import given, when, then
import requests
import re
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
    # Instead of assuming ID 1, let's fetch first available category
    response = context.api_session.get(f"{context.base_api_url}/products/categories")
    categories = response.json()
    if categories:
        context.valid_cat_id = categories[0]['id']
    else:
        assert False, "No categories found in database"

import random

@when('I create a product with name "{name}", price {price:d}, stock {stock:d}, and details "{details}"')
def step_impl(context, name, price, stock, details):
    cat_id = getattr(context, 'valid_cat_id', 1)
    unique_name = f"{name} {random.randint(1000, 9999)}"
    payload = {
        "name": unique_name,
        "price": float(price),
        "stock": stock,
        "category_id": cat_id,
        "details": details
    }
    context.response = context.api_session.post(f"{context.base_api_url}/products/", json=payload)

@when('I create a product with name "{name}", price {price:d}, stock {stock:d}, and no image URL')
def step_impl(context, name, price, stock):
    cat_id = getattr(context, 'valid_cat_id', 1)
    payload = {
        "name": name,
        "price": float(price),
        "stock": stock,
        "category_id": cat_id,
        "image_url": None
    }
    context.response = context.api_session.post(f"{context.base_api_url}/products/", json=payload)

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

@when('I click on product "{name}"')
def step_impl(context, name):
    context.page.locator('.product-card', has_text=name).first.click()

@then('I should see the product detail page for "{name}"')
def step_impl(context, name):
    expect(context.page.locator('h1')).to_contain_text(name)
    expect(context.page).to_have_url(re.compile(r".*/products/\d+"))

@then('I should see the product story "{text}"')
def step_impl(context, text):
    expect(context.page.locator('.details-content')).to_contain_text(text)

@when('I fill in the product form with name "{name}", price {price:d}, stock {stock:d}, and details "{details}"')
def step_impl(context, name, price, stock, details):
    # Open the add modal first
    context.page.click('#add-product-btn')
    
    # Wait for modal content
    try:
        context.page.wait_for_selector('.modal-content', state='visible', timeout=5000)
        
        # Fill based on labels or IDs
        context.page.get_by_label("Product Name").fill(name)
        context.page.get_by_label("Price (₹)").fill(str(price))
        context.page.get_by_label("Stock").fill(str(stock))
        # Select category - assuming first option
        context.page.get_by_label("Category").select_option(index=1)
        context.page.get_by_label("Detailed Product Story").fill(details)
    except Exception as e:
        context.page.screenshot(path="error_admin_modal_details.png")
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
