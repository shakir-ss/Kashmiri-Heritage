from behave import given, when, then
import requests
from playwright.sync_api import expect

# --- API STEPS ---

@given('a product exists with ID {prod_id:d}')
def step_impl(context, prod_id):
    pass

@when('I add {quantity:d} units of product {prod_id:d} to the cart')
@when('I add {quantity:d} unit of product {prod_id:d} to the cart')
def step_impl(context, quantity, prod_id):
    payload = {"product_id": prod_id, "quantity": quantity}
    context.response = context.api_session.post(f"{context.base_api_url}/cart/add", json=payload)

@then('the cart should contain {quantity:d} units of product {prod_id:d}')
def step_impl(context, quantity, prod_id):
    response = context.api_session.get(f"{context.base_api_url}/cart/")
    cart_items = response.json()
    # Assuming the API returns a list of items for the user
    item = next((i for i in cart_items if i['product_id'] == prod_id), None)
    assert item is not None
    assert item['quantity'] == quantity

@given('my cart contains items')
def step_impl(context):
    payload = {"product_id": 1, "quantity": 1}
    context.api_session.post(f"{context.base_api_url}/cart/add", json=payload)

@when('I place an order with address "{address}" and phone "{phone}"')
def step_impl(context, address, phone):
    payload = {"address": address, "phone": phone}
    context.response = context.api_session.post(f"{context.base_api_url}/orders/place", json=payload)

@then('the order should be created successfully')
def step_impl(context):
    assert context.response.status_code == 201
    assert "order_id" in context.response.json()

@then('the cart should be cleared')
def step_impl(context):
    response = context.api_session.get(f"{context.base_api_url}/cart/")
    assert len(response.json()) == 0

# --- UI STEPS ---

@given('I am on the Home page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/")

@when('I add "{name}" to the cart')
def step_impl(context, name):
    # Find the card with the name, and click its Add to Cart button (use first if multiple)
    product_card = context.page.locator('.product-card', has_text=name).first
    product_card.get_by_text("Add to Cart").click()
    
    try:
        # Wait for the cart badge to show items (assuming it's .cart-badge)
        context.page.wait_for_selector('.cart-badge', timeout=5000)
    except Exception as e:
        context.page.screenshot(path="error_add_to_cart.png")
        # Print page content to see what's actually there
        # print(context.page.content())
        raise e
    
    # Wait for potential animation or state update
    context.page.wait_for_timeout(1000)

@when('I go to the Cart page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/cart")
    # Wait for the summary or empty cart message to appear
    context.page.wait_for_load_state("networkidle")
    # Take a screenshot to see if the cart is empty or items are there
    context.page.screenshot(path="debug_cart_page.png")
    # Assert that we are NOT seeing the empty cart message if we expect items
    expect(context.page.locator('.empty-cart')).not_to_be_visible()

@when('I fill in address "{address}" and phone "{phone}"')
def step_impl(context, address, phone):
    context.page.screenshot(path="debug_checkout_page.png")
    context.page.fill('textarea[placeholder="House/Apt No, Street, City, Pincode"]', address)
    context.page.fill('input[placeholder="+91 XXXX XXX XXX"]', phone)

@then('I should see "{message}"')
def step_impl(context, message):
    try:
        # Wait a bit longer for the mock payment + backend call
        context.page.wait_for_timeout(2000)
        expect(context.page.get_by_text(message).first).to_be_visible(timeout=10000)
    except Exception as e:
        context.page.screenshot(path=f"error_see_{message.replace(' ', '_')}.png")
        raise e

@then('I should see my order in the order history')
def step_impl(context):
    # SuccessOrder screen has a link or we can just go to /orders if implemented
    # For now, let's just check if the success screen stays visible or navigate
    context.page.goto(f"{context.base_ui_url}/orders")
    context.page.wait_for_load_state("networkidle")
    # Assuming .order-card exists in the order history view
    expect(context.page.locator('.order-card').first).to_be_visible(timeout=10000)
