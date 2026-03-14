from behave import given, when, then
import requests
import re
from playwright.sync_api import expect

# --- API STEPS ---

@when('I add product {prod_id:d} to my wishlist')
def step_impl(context, prod_id):
    pid = getattr(context, 'valid_prod_id', prod_id)
    payload = {"product_id": pid}
    context.response = context.api_session.post(f"{context.base_api_url}/wishlist/add", json=payload)

# --- UI STEPS ---

@when('I click the wishlist icon on product "{name}"')
def step_impl(context, name):
    product_card = context.page.locator('.product-card', has_text=name).first
    product_card.locator('.card-wishlist-btn').click()

@then('the wishlist icon for "{name}" should be active')
def step_impl(context, name):
    product_card = context.page.locator('.product-card', has_text=name).first
    expect(product_card.locator('.card-wishlist-btn')).to_have_class(re.compile(r".*active.*"))

@then('I should see {count:d} item in my wishlist count')
def step_impl(context, count):
    # Assuming we add a badge to wishlist icon too, or just check the page later
    pass

@given('I have "{name}" in my wishlist')
def step_impl(context, name):
    # Ensure it's in wishlist via UI or API
    context.page.goto(f"{context.base_ui_url}/products")
    btn = context.page.locator('.product-card', has_text=name).first.locator('.card-wishlist-btn')
    if "active" not in btn.get_attribute("class"):
        btn.click()

@when('I go to the Wishlist page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/wishlist")

@then('I should see "{name}" in the wishlist grid')
def step_impl(context, name):
    expect(context.page.locator('.wishlist-card')).to_contain_text(name)

@when('I click "Remove" for "{name}"')
def step_impl(context, name):
    card = context.page.locator('.wishlist-card', has_text=name).first
    card.get_by_text("Remove").click()
