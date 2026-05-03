"""
lifecycle_steps.py — Steps for: address_book.feature, reorder_b2b.feature
Updated to use dynamic base_api_url from environment.py
"""
from behave import given, when, then
import requests
from playwright.sync_api import expect

# ============================================================
# ADDRESS BOOK STEPS
# ============================================================

@given('I am logged in as a regular customer via API')
def step_impl(context):
    import random
    email = f"customer_{random.randint(1000, 9999)}@test.com"
    requests.post(f"{context.base_api_url}/auth/register", json={
        "name": "Test Customer", "email": email, "password": "testpass123"
    })
    login_res = requests.post(f"{context.base_api_url}/auth/login", json={
        "email": email, "password": "testpass123"
    })
    token = login_res.json()['token']
    context.api_session.headers.update({"Authorization": f"Bearer {token}"})

@when('I save an address with name "{name}", line "{line}", city "{city}", state "{state}", pincode "{pincode}"')
def step_impl(context, name, line, city, state, pincode):
    context.response = context.api_session.post(f"{context.base_api_url}/auth/addresses", json={
        "name": name,
        "phone": "9988776655",
        "address_line": line,
        "city": city,
        "state": state,
        "country": "India",
        "pincode": pincode,
        "is_default": True
    })

@given('I have at least one saved address')
def step_impl(context):
    context.api_session.post(f"{context.base_api_url}/auth/addresses", json={
        "name": "Test Address",
        "phone": "9988776655",
        "address_line": "12 Test Lane",
        "city": "Srinagar",
        "state": "Jammu & Kashmir",
        "country": "India",
        "pincode": "190001",
        "is_default": True
    })

@when('I fetch my saved addresses via API')
def step_impl(context):
    context.response = context.api_session.get(f"{context.base_api_url}/auth/addresses")

@then('the API should return a list of addresses')
def step_impl(context):
    data = context.response.json()
    assert isinstance(data, list), f"Expected a list, got: {data}"
    assert len(data) >= 1, "Address list is empty"

@when('I delete my first saved address via API')
def step_impl(context):
    addresses = context.api_session.get(f"{context.base_api_url}/auth/addresses").json()
    assert len(addresses) >= 1, "No addresses to delete"
    addr_id = addresses[0]['id']
    context.response = context.api_session.delete(f"{context.base_api_url}/auth/addresses/{addr_id}")

@when('I request my saved addresses without authentication')
def step_impl(context):
    context.response = requests.get(f"{context.base_api_url}/auth/addresses")

@given('I have a saved address "{label}" in my address book')
def step_impl(context, label):
    login_res = requests.post(f"{context.base_api_url}/auth/login", json={
        "email": "root@thehundredvillages.com", "password": "root123"
    })
    token = login_res.json()['token']
    requests.post(f"{context.base_api_url}/auth/addresses", json={
        "name": label,
        "phone": "9988776655",
        "address_line": "Dal Lake View",
        "city": "Srinagar",
        "state": "Jammu & Kashmir",
        "country": "India",
        "pincode": "190001",
        "is_default": True
    }, headers={"Authorization": f"Bearer {token}"})

@when('I navigate to the checkout page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/products")
    context.page.wait_for_selector('.product-card', state='visible', timeout=15000)
    btn = context.page.locator('.product-card').first.locator('button.btn-primary')
    btn.click()
    context.page.wait_for_timeout(1000)
    context.page.goto(f"{context.base_ui_url}/checkout")
    context.page.wait_for_load_state("networkidle")
    context.page.wait_for_timeout(2000)

@then('I should see the address dropdown with "{label}"')
def step_impl(context, label):
    dropdown = context.page.locator('.address-book-selector select')
    expect(dropdown).to_be_visible(timeout=8000)
    options_text = dropdown.inner_text()
    assert label in options_text, f"Address '{label}' not found in dropdown: {options_text}"

@when('I select "{label}" from the saved addresses dropdown')
def step_impl(context, label):
    context.page.locator('.address-book-selector select').select_option(label=label)
    context.page.wait_for_timeout(1500)

@then('the city field should be pre-filled with the saved city')
def step_impl(context):
    city_value = context.page.locator('input#city').input_value()
    assert city_value.strip() != '', "City field is empty after selecting saved address"

# ============================================================
# REORDER STEPS
# ============================================================

@when('I fetch my order history via API')
def step_impl(context):
    context.response = context.api_session.get(f"{context.base_api_url}/orders/")
    context.orders_data = context.response.json()

@then('each order item should contain a "{field}" field')
def step_impl(context, field):
    orders = context.orders_data
    assert len(orders) > 0, "No orders found"
    for order in orders:
        for item in order.get('items', []):
            assert field in item, f"Field '{field}' missing from order item: {item}"

@given('I have at least one past order')
def step_impl(context):
    orders_res = context.api_session.get(f"{context.base_api_url}/orders/")
    assert orders_res.status_code == 200 and len(orders_res.json()) > 0, \
        "No past orders available for reorder test"

@when('I click "Buy Again" for the first past order')
def step_impl(context):
    buy_again_btn = context.page.locator('button', has_text='Buy Again').first
    buy_again_btn.scroll_into_view_if_needed()
    buy_again_btn.click()
    context.page.wait_for_timeout(2000)

@then('I should be redirected to the cart page')
def step_impl(context):
    context.page.wait_for_url(f"{context.base_ui_url}/cart", timeout=10000)

@then('the cart should contain items from the past order')
def step_impl(context):
    cart_items = context.page.locator('.cart-item, .summary-item')
    expect(cart_items.first).to_be_visible(timeout=8000)

# ============================================================
# B2B WHOLESALE STEPS
# ============================================================

@when('I click the "Wholesale" link in the navigation')
def step_impl(context):
    context.page.locator('nav a', has_text='Wholesale').first.click()
    context.page.wait_for_load_state("networkidle")

@then('I should be on the Wholesale page')
def step_impl(context):
    expect(context.page).to_have_url(f"{context.base_ui_url}/wholesale", timeout=8000)

@given('I am on the Wholesale page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/wholesale")
    context.page.wait_for_load_state("networkidle")
    context.page.wait_for_timeout(1500)

@when('I submit a B2B inquiry with company "{company}", email "{email}", phone "{phone}", and requirements "{requirements}"')
def step_impl(context, company, email, phone, requirements):
    context.response = requests.post(f"{context.base_api_url}/orders/b2b/inquiry", json={
        "company_name": company,
        "email": email,
        "phone": phone,
        "requirements": requirements
    })

@when('I fill in the wholesale form with company "{company}", email "{email}", phone "{phone}", and requirements "{requirements}"')
def step_impl(context, company, email, phone, requirements):
    page = context.page
    page.locator('input[placeholder*="company" i], input[id*="company" i]').first.fill(company)
    page.locator('input[type="email"]').first.fill(email)
    page.locator('input[type="tel"], input[placeholder*="phone" i]').first.fill(phone)
    page.locator('textarea').first.fill(requirements)

@when('I click "Submit Inquiry" on the wholesale form')
def step_impl(context):
    btn = context.page.locator('button[type="submit"], button', has_text='Submit').first
    btn.scroll_into_view_if_needed()
    btn.click()
    context.page.wait_for_timeout(2000)

@then('I should see "Thank you" or "submitted" on the page')
def step_impl(context):
    body = context.page.locator('body')
    try:
        expect(body).to_contain_text('Thank you', timeout=5000)
    except:
        expect(body).to_contain_text('submitted', timeout=5000)

# ============================================================
# NAVIGATE STEPS  (not already defined elsewhere)
# ============================================================

@when('I navigate to the orders page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/orders")
    context.page.wait_for_load_state("networkidle")
    context.page.wait_for_timeout(2000)
