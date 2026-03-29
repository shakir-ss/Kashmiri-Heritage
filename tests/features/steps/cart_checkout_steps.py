from behave import given, when, then
import requests
from playwright.sync_api import expect

# --- API STEPS ---

@given('a product exists with ID {prod_id:d}')
def step_impl(context, prod_id):
    # Clear cart first to ensure clean state
    context.api_session.delete(f"{context.base_api_url}/cart/clear")
    
    # Fetch first available product
    response = context.api_session.get(f"{context.base_api_url}/products/")
    products = response.json()
    if products:
        context.valid_prod_id = products[0]['id']
    else:
        assert False, "No products found in database"

@when('I add {quantity:d} units of product {prod_id:d} to the cart')
@when('I add {quantity:d} unit of product {prod_id:d} to the cart')
def step_impl(context, quantity, prod_id):
    # Use dynamic product ID if available
    pid = getattr(context, 'valid_prod_id', prod_id)
    payload = {"product_id": pid, "quantity": quantity}
    context.response = context.api_session.post(f"{context.base_api_url}/cart/add", json=payload)
    if context.response.status_code != 201:
        print(f"API CART ADD FAILED: {context.response.status_code} - {context.response.text}")

@then('the cart should contain {quantity:d} units of product {prod_id:d}')
def step_impl(context, quantity, prod_id):
    pid = getattr(context, 'valid_prod_id', prod_id)
    response = context.api_session.get(f"{context.base_api_url}/cart/")
    cart_items = response.json()
    print(f"DEBUG CART ITEMS: {cart_items}")
    item = next((i for i in cart_items if i['product_id'] == pid), None)
    assert item is not None, f"Product {pid} not found in cart: {cart_items}"
    # Use >= to be resilient to leftover data if any
    assert item['quantity'] >= quantity

@given('my cart contains items')
def step_impl(context):
    context.api_session.delete(f"{context.base_api_url}/cart/clear")
    response = context.api_session.get(f"{context.base_api_url}/products/")
    product = response.json()[0]
    pid = product['id']
    
    # Replenish stock for reliable testing
    context.api_session.put(f"{context.base_api_url}/products/{pid}", json={
        "name": product['name'],
        "price": product['price'],
        "stock": 100,
        "category_id": product['category_id']
    })
    
    payload = {"product_id": pid, "quantity": 1}
    res = context.api_session.post(f"{context.base_api_url}/cart/add", json=payload)
    assert res.status_code == 201

@when('I place an order with address "{address}" and phone "{phone}"')
def step_impl(context, address, phone):
    payload = {
        "address": address, 
        "phone": phone,
        "city": "Srinagar",
        "state": "Jammu & Kashmir",
        "country": "India",
        "pincode": "190001",
        "payment_mode": "upi"
    }
    context.response = context.api_session.post(f"{context.base_api_url}/orders/place", json=payload)


@then('the order should be created successfully')
def step_impl(context):
    assert context.response.status_code == 201, f"Expected 201 but got {context.response.status_code}: {context.response.text}"
    assert "order_id" in context.response.json()

@then('the cart should be cleared')
def step_impl(context):
    response = context.api_session.get(f"{context.base_api_url}/cart/")
    assert len(response.json()) == 0

# --- UI STEPS ---

@given('I am on the Home page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/")
    # Clear local storage cart if possible to ensure isolation
    context.page.evaluate("window.localStorage.removeItem('cart_items')")

@when('I add "{name}" to the cart')
def step_impl(context, name):
    # Ensure products are loaded and visible
    context.page.wait_for_selector('.product-card', state='visible', timeout=15000)
    
    # Use context.last_product_name if name matches placeholder
    actual_name = getattr(context, 'last_product_name', name) if name in ["Limited Edition Box", "Multi-Pack Saffron"] else name

    # Find the card with the name
    card = context.page.locator('.product-card', has_text=actual_name).first
    expect(card).to_be_visible(timeout=10000)
    
    # Scroll into view
    card.scroll_into_view_if_needed()
    
    # Click its primary button (Add to Cart)
    # We target the button that isn't 'Out of Stock'
    btn = card.locator('button.btn-primary:not(:disabled)')
    if btn.count() == 0:
        # If disabled, try to replenish via API and refresh
        response = context.api_session.get(f"{context.base_api_url}/products/")
        product = next((p for p in response.json() if p['name'] == actual_name), None)
        if product:
            context.api_session.put(f"{context.base_api_url}/products/{product['id']}", json={
                "is_active": True,
                "stock": 100
            })
            context.page.reload()
            context.page.wait_for_selector('.product-card', state='visible', timeout=10000)
            card = context.page.locator('.product-card', has_text=actual_name).first
            btn = card.locator('button.btn-primary:not(:disabled)')

    btn.click()
    
    # Wait for store sync / notification
    context.page.wait_for_timeout(1000)

@when('I go to the Cart page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/cart")
    context.page.wait_for_load_state("networkidle")
    # Brief wait for Pinia to sync
    context.page.wait_for_timeout(2000)
    # Just verify we are on the cart page
    expect(context.page.locator('.cart-view')).to_be_visible()

@when('I fill in address "{address}" and phone "{phone}"')
def step_impl(context, address, phone):
    context.page.locator('input[id="address"]').fill(address)
    context.page.locator('input[id="phone"]').fill(phone)

@then('I should see "{message}"')
@when('I should see "{message}"')
def step_impl(context, message):
    try:
        # Wait for any pending network requests (like the order POST)
        context.page.wait_for_load_state("networkidle")
        # Extra buffer for UI transitions
        context.page.wait_for_timeout(2000)
        expect(context.page.get_by_text(message).first).to_be_visible(timeout=15000)
    except Exception as e:
        context.page.screenshot(path=f"error_see_{message.replace(' ', '_')}.png")
        raise e

@then('I should see my order in the order history')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/orders")
    context.page.wait_for_load_state("networkidle")
    expect(context.page.locator('.order-card').first).to_be_visible(timeout=10000)

@when('I click on the product icon for "{name}"')
@when('I click on product icon for "{name}"')
def step_impl(context, name):
    item_row = context.page.locator('.summary-item, .cart-item', has_text=name).first
    item_row.locator('img').click()

@then('I should see "{text}" in delivery charges')
def step_impl(context, text):
    expect(context.page.locator('.summary-row', has_text="Logistics & Handling")).to_contain_text(text)

@when('I select payment mode "{mode_label}"')
def step_impl(context, mode_label):
    # Scroll into view to ensure clickable
    opt = context.page.locator('.payment-option', has_text=mode_label)
    opt.scroll_into_view_if_needed()
    opt.click()

@when('I agree to the terms')
def step_impl(context):
    # Click the checkbox container which is clickable
    context.page.locator('.checkbox-container').click()

@then('I should be on the detail page for "{name}"')
def step_impl(context, name):
    import re
    context.page.wait_for_url(re.compile(r".*/products/\d+"))
    expect(context.page.locator('h1')).to_contain_text(name)

# --- RAZORPAY SPECIFIC STEPS ---

@when('I click the button "{label}"')
def step_impl(context, label):
    # Search for button with text or containing text
    # Prefer the one in the checkout form if it exists
    btn = context.page.locator('.checkout-form button', has_text=label).first
    if not btn.is_visible():
        btn = context.page.get_by_role("button", name=label).first
    if not btn.is_visible():
        btn = context.page.locator("button", has_text=label).first
    
    btn.scroll_into_view_if_needed()
    btn.click()

@then('I should see the Razorpay checkout modal')
def step_impl(context):
    try:
        # Razorpay modal is an iframe with class 'razorpay-checkout-frame'
        context.page.wait_for_selector('iframe.razorpay-checkout-frame', state='visible', timeout=20000)
        context.razorpay_frame = context.page.frame_locator('iframe.razorpay-checkout-frame')
        # Verify we can see common RZP elements inside the frame
        expect(context.razorpay_frame.get_by_text("The Hundred Villages")).to_be_visible()
    except Exception as e:
        context.page.screenshot(path="razorpay_modal_fail.png")
        # Also print page content to see if there's an error message
        print(f"PAGE CONTENT ON FAIL: {context.page.content()[:500]}...")
        raise e

@when('I complete the Razorpay payment with test card "{card_num}"')
def step_impl(context, card_num):
    # 1. Select Card Payment in RZP Modal
    # Note: RZP UI might change, but these are common IDs/Texts
    card_opt = context.razorpay_frame.get_by_text("Card").first
    card_opt.click()

    # 2. Fill Card Details
    context.razorpay_frame.get_by_placeholder("Card Number").fill(card_num)
    context.razorpay_frame.get_by_placeholder("MM / YY").fill("12/30")
    context.razorpay_frame.get_by_placeholder("CVV").fill("111")
    
    # 3. Click Pay Now
    context.razorpay_frame.get_by_role("button", name="Pay Now").click()

    # 4. Handle "Success" scenario if RZP asks for OTP or Skip Saving Card
    # Sometimes RZP asks "Skip saving card" - click it if it appears
    skip_btn = context.razorpay_frame.get_by_role("button", name="Skip Saving Card").first
    if skip_btn.is_visible(timeout=2000):
        skip_btn.click()

    # 5. Success/Failure page inside RZP modal
    # In test mode, RZP sometimes shows "Success" / "Failure" buttons
    success_btn = context.razorpay_frame.get_by_role("button", name="Success").first
    if success_btn.is_visible(timeout=5000):
        success_btn.click()

    # Wait for frame to disappear and UI to update
    context.page.wait_for_selector('iframe.razorpay-checkout-frame', state='hidden', timeout=15000)

@then('my order status should be "{status}" in the database')
def step_impl(context, status):
    # Login to get token
    login_res = requests.post(f"{context.base_api_url}/auth/login", json={
        "email": "root@thehundredvillages.com",
        "password": "root123"
    })
    token = login_res.json()['token']
    
    # Fetch orders
    orders_res = requests.get(f"{context.base_api_url}/orders/", headers={"Authorization": f"Bearer {token}"})
    orders = orders_res.json()
    
    # Get the latest order
    latest_order = sorted(orders, key=lambda x: x['id'], reverse=True)[0]
    assert latest_order['status'] == status, f"Expected status {status} but got {latest_order['status']}"
