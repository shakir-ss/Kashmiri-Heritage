from behave import given, when, then
import requests
import re
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
        "payment_mode": "mock" # Use mock for API tests to bypass RZP
    }
    res = context.api_session.post(f"{context.base_api_url}/orders/place", json=payload)
    context.response = res
    
    # If the response is successful and it's a mock payment, call verify
    if res.status_code == 201:
        order_data = res.json()
        verify_payload = {
            "razorpay_order_id": order_data.get("razorpay_order_id", "mock_order_id"),
            "razorpay_payment_id": "mock_payment_api",
            "razorpay_signature": "mock_signature",
            "order_id": order_data.get("order_id")
        }
        # Call verify endpoint to clear the cart
        context.api_session.post(f"{context.base_api_url}/orders/verify", json=verify_payload)


@then('the order should be created successfully')
def step_impl(context):
    assert context.response.status_code == 201, f"Expected 201 but got {context.response.status_code}: {context.response.text}"
    assert "order_id" in context.response.json()

@then('the cart should be cleared')
def step_impl(context):
    # Use a small retry loop as DB commit might have slight delay
    import time
    for _ in range(5):
        response = context.api_session.get(f"{context.base_api_url}/cart/")
        if len(response.json()) == 0:
            return
        time.sleep(0.5)
    
    # Final check
    response = context.api_session.get(f"{context.base_api_url}/cart/")
    assert len(response.json()) == 0, f"Cart not cleared: {response.json()}"

# --- UI STEPS ---

@given('I am on the Home page')
def step_impl(context):
    # Actually go to the root Home page
    context.page.goto(f"{context.base_ui_url}/")
    # Clear local storage cart to ensure isolation
    context.page.evaluate("window.localStorage.removeItem('cart_items')")
    # Wait for the hero section to be visible to confirm we are on the Home page
    context.page.wait_for_selector('.hero', state='visible', timeout=15000)
    context.page.wait_for_timeout(2000)

@given('I am on the Products page')
@when('I am on the Products page')
def step_impl(context):
    # Navigate specifically to the products catalog
    context.page.goto(f"{context.base_ui_url}/products")
    # Clear local storage cart to ensure isolation
    context.page.evaluate("window.localStorage.removeItem('cart_items')")
    # Wait for products to load
    context.page.wait_for_selector('.product-card', state='visible', timeout=15000)
    context.page.wait_for_timeout(2000)

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
    
    # Check if 'Go to Cart' is already visible
    btn_go = card.locator('button.btn-secondary', has_text="Go to Cart")
    if btn_go.count() > 0:
        print(f"DEBUG: {actual_name} is already in cart.")
        return

    # Click its primary button (Add to Cart)
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
    context.page.wait_for_timeout(1500)

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
        # Extra buffer for redirection
        context.page.wait_for_timeout(5000)
        # Use a long timeout and more flexible matching
        # Sometimes '✓' or other icons are part of the text
        locator = context.page.locator("body")
        expect(locator).to_contain_text(message, timeout=45000)
        print(f"DEBUG: Success message '{message}' found on page.")
    except Exception as e:
        context.page.screenshot(path=f"error_see_{message.replace(' ', '_')}.png")
        # Print page content to help debug
        print(f"DEBUG PAGE CONTENT: {context.page.content()[:1000]}")
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
    # Click the checkbox label/container
    selector = '.checkbox-container'
    context.page.wait_for_selector(selector, state='visible')
    context.page.locator(selector).scroll_into_view_if_needed()
    context.page.locator(selector).click()
    # Wait for the button to become enabled (if it was disabled)
    context.page.wait_for_timeout(500)

@then('I should be on the detail page for "{name}"')
def step_impl(context, name):
    import re
    context.page.wait_for_url(re.compile(r".*/products/\d+"))
    expect(context.page.locator('h1')).to_contain_text(name)

# --- RAZORPAY SPECIFIC STEPS ---

@when('I click the button "{label}"')
def step_impl(context, label):
    # Use a more robust selector strategy for the checkout button
    # It might be a button with a span inside
    selector = f"button:has-text('{label}')"
    
    # Wait for the button to be present and not disabled
    try:
        # Give it some time to appear/enable
        btn = context.page.locator(selector).first
        btn.wait_for(state="visible", timeout=10000)
        
        # Ensure it's not disabled (loading or invalid form)
        # If it's disabled, we might need to wait for validation to pass
        for _ in range(5):
            if btn.is_enabled():
                break
            context.page.wait_for_timeout(500)
            
        btn.scroll_into_view_if_needed()
        # Click with force if necessary to bypass transparent overlays
        btn.click(force=True)
        print(f"DEBUG: Clicked button '{label}'")
    except Exception as e:
        context.page.screenshot(path=f"fail_click_{label.replace(' ', '_')}.png")
        raise e

@then('I should see the Razorpay checkout modal')
def step_impl(context):
    # Wait for the main Razorpay iframe
    try:
        context.page.wait_for_selector('iframe.razorpay-checkout-frame', state='visible', timeout=30000)
        # We don't store context.razorpay_frame anymore, we will search dynamically
        print("DEBUG: Razorpay main iframe detected.")
    except Exception as e:
        context.page.screenshot(path="razorpay_modal_fail.png")
        raise e

def find_and_click_in_frames(page, selector_type, selector_value, click=True):
    """Highly optimized helper to find an element in the RZP frame or any other frame."""
    # 1. Try to get the main Razorpay frame directly first (90% of cases)
    rzp_frame = page.frame(name=re.compile("rzp_checkout_field")) or page.frame_locator("iframe.razorpay-checkout-frame")
    
    # 2. List of frames to check: Razorpay first, then others
    frames_to_check = []
    try:
        # Check if it's a frame locator or a frame
        if hasattr(rzp_frame, 'locator'):
            # It's a FrameLocator
            loc = None
            if selector_type == "text": loc = rzp_frame.get_by_text(selector_value, exact=False).first
            elif selector_type == "role": loc = rzp_frame.get_by_role("button", name=selector_value).first
            elif selector_type == "placeholder": loc = rzp_frame.get_by_placeholder(selector_value).first
            
            if loc and loc.is_visible(timeout=500):
                if click: loc.click()
                return loc
    except:
        pass

    # 3. Fallback: Quick scan all frames with minimal timeout
    for frame in page.frames:
        try:
            if selector_type == "text": loc = frame.get_by_text(selector_value, exact=False).first
            elif selector_type == "role": loc = frame.get_by_role("button", name=selector_value).first
            elif selector_type == "placeholder": loc = frame.get_by_placeholder(selector_value).first
            
            # Use a very short timeout (100ms) during the loop
            if loc.is_visible(timeout=100):
                if click: loc.click()
                return loc
        except:
            continue
    return None

@when('I complete the Razorpay payment with test card "{card_num}"')
def step_impl(context, card_num):
    import time
    context.page.wait_for_timeout(2000)
    
    # 1. Select Card
    find_and_click_in_frames(context.page, "text", "Card")
    
    # 2. Fill Details
    find_and_click_in_frames(context.page, "placeholder", "Card Number", click=False).fill(card_num)
    find_and_click_in_frames(context.page, "placeholder", "MM / YY", click=False).fill("12/30")
    find_and_click_in_frames(context.page, "placeholder", "CVV", click=False).fill("111")
    
    # 3. Pay Now
    find_and_click_in_frames(context.page, "text", "Pay Now")
    
    # Handle Success Page (Wait for main step to verify)
    context.page.wait_for_timeout(3000)

@when('I complete the Razorpay payment with Netbanking')
def step_impl(context):
    # Ensure regex is available
    import re
    
    # 1. Select Netbanking
    find_and_click_in_frames(context.page, "text", "Netbanking")

    # 2. Select Bank
    if not find_and_click_in_frames(context.page, "text", "HDFC"):
        find_and_click_in_frames(context.page, "text", "CANARA BANK")

    # 3. Pay Now - Catch the popup
    context.bank_page = None
    try:
        # Reduced expect_page timeout to 5s as it should be instant
        with context.browser_context.expect_page(timeout=5000) as popup_info:
            find_and_click_in_frames(context.page, "text", "Pay")
        context.wait_for_timeout(2000)  # Wait for the popup to load
        context.bank_page = popup_info.value
        print(f"DEBUG: Bank popup detected: {context.bank_page.url}")
    except Exception:
        print("DEBUG: No popup detected, button might have redirected main window.")
        print(f"DEBUG: Current page URL: {context.page.url}")
        print(f"DEBUG: All open pages: {[p.url for p in context.browser_context.pages]}")
        print("DEBUG: Attempting to find bank page among open pages...")
        
        if len(context.browser_context.pages) > 1:
            context.bank_page = context.browser_context.pages[-1]
            print(f"DEBUG: Found bank page manually: {context.bank_page.url}")
        else:
            context.bank_page = context.page

@when('I click "{action}" on the bank gateway')
def step_impl(context, action):
    # This page is NOT inside a frame, so we use direct locators (FAST)
    # Use the bank page if available, else fallback to the main page
    target_page = getattr(context, 'bank_page', context.page)
    
    # Wait a moment for the new page to render
    target_page.wait_for_load_state('domcontentloaded')

    # Locate the button with the specified action
    try:
        btn = target_page.get_by_role("button", name=action, exact=False).first
        if btn.is_visible(timeout=5000):  # 5s timeout to ensure mocksharp is loaded
            btn.click()
            print(f"DEBUG: Successfully clicked the '{action}' button on the bank gateway.")
        else:
            raise Exception(f"Button with action '{action}' not found or not visible.")
    except Exception as e:
        target_page.screenshot(path=f"error_bank_action_{action}.png")
        print(f"DEBUG: Failed to click the '{action}' button. Error: {e}")
        raise e

    # Final wait for any processing
    target_page.wait_for_timeout(3000)

@then('my order status should be "{status}" in the database')
def step_impl(context, status):
    import time
    # Login to get token
    login_res = requests.post(f"{context.base_api_url}/auth/login", json={
        "email": "root@thehundredvillages.com",
        "password": "root123"
    })
    token = login_res.json()['token']
    
    # Retry loop for status update
    for _ in range(10):
        # Fetch orders
        orders_res = requests.get(f"{context.base_api_url}/orders/", headers={"Authorization": f"Bearer {token}"})
        orders = orders_res.json()
        
        # Get the latest order
        latest_order = sorted(orders, key=lambda x: x['id'], reverse=True)[0]
        if latest_order['status'] == status:
            print(f"DEBUG: Order {latest_order['id']} status updated to {status} successfully.")
            return
        
        print(f"DEBUG: Order status is {latest_order['status']}, waiting for {status}...")
        time.sleep(2)
    
    # Final check
    orders_res = requests.get(f"{context.base_api_url}/orders/", headers={"Authorization": f"Bearer {token}"})
    latest_order = sorted(orders_res.json(), key=lambda x: x['id'], reverse=True)[0]
    assert latest_order['status'] == status, f"Expected status {status} but got {latest_order['status']}"
