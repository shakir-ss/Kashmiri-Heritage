"""
promo_rma_steps.py — Steps for: promo_engine.feature, rma_returns.feature
Updated to use dynamic base_api_url from environment.py
"""
from behave import given, when, then
import requests
import time

# ============================================================
# PROMO CODE STEPS
# ============================================================

@given('a promo code "{code}" exists with {discount:d} percent discount')
def step_impl(context, code, discount):
    """Ensure the promo code exists; if not, create it via admin API."""
    res = context.api_session.post(f"{context.base_api_url}/orders/promo/create", json={
        "code": code,
        "discount_percent": discount,
        "max_uses": 9999
    })
    # Ignore 409 conflict (already exists) — we just need it to exist
    assert res.status_code in [201, 409, 200], f"Failed to ensure promo code: {res.text}"

@given('a promo code "{code}" exists with 0 remaining uses')
def step_impl(context, code):
    """Create a maxed-out promo code."""
    context.api_session.post(f"{context.base_api_url}/orders/promo/create", json={
        "code": code,
        "discount_percent": 10,
        "max_uses": 0,
        "current_uses": 0
    })

@when('I apply promo code "{code}" via API')
def step_impl(context, code):
    # Route is /promo/validate
    context.response = context.api_session.post(
        f"{context.base_api_url}/orders/promo/validate",
        json={"promo_code": code}
    )

@then('the API should return a discount percentage of {discount:d}')
def step_impl(context, discount):
    data = context.response.json()
    assert 'discount_percent' in data, f"No discount_percent in response: {data}"
    assert data['discount_percent'] == discount, \
        f"Expected discount {discount} but got {data['discount_percent']}"

@when('I enter promo code "{code}" and click Apply')
def step_impl(context, code):
    promo_input = context.page.locator('input[placeholder*="promo" i], input[placeholder*="coupon" i]').first
    promo_input.scroll_into_view_if_needed()
    promo_input.fill(code)
    apply_btn = context.page.locator('button', has_text='Apply').first
    apply_btn.click()
    context.page.wait_for_timeout(1500)

@then('I should see a discount applied in the order summary')
def step_impl(context):
    from playwright.sync_api import expect
    discount_row = context.page.locator('.summary-row, .promo-row', has_text='Discount')
    expect(discount_row).to_be_visible(timeout=8000)

@then('I should see "{text}" confirmed on the page')
def step_impl(context, text):
    from playwright.sync_api import expect
    expect(context.page.locator('body')).to_contain_text(text, timeout=10000)

# ============================================================
# RMA / RETURN REQUEST STEPS
# ============================================================

@given('I have a delivered order')
def step_impl(context):
    """Find or create an order and force its status to delivered."""
    orders_res = context.api_session.get(f"{context.base_api_url}/orders/")
    orders = orders_res.json()
    if orders:
        order = orders[0]
        context.test_order_id = order['id']
        # Force status to delivered
        context.api_session.put(
            f"{context.base_api_url}/orders/{order['id']}/status",
            json={"status": "Delivered"}
        )
    else:
        assert False, "No orders available to test RMA"

@given('I have a pending order')
def step_impl(context):
    orders_res = context.api_session.get(f"{context.base_api_url}/orders/")
    orders = orders_res.json()
    if orders:
        order = orders[0]
        context.test_order_id = order['id']
        context.api_session.put(
            f"{context.base_api_url}/orders/{order['id']}/status",
            json={"status": "Pending"}
        )
    else:
        assert False, "No orders available to test RMA"

@when('I submit a return request for the order with reason "{reason}"')
def step_impl(context, reason):
    order_id = context.test_order_id
    context.response = context.api_session.post(
        f"{context.base_api_url}/orders/{order_id}/return",
        json={"reason": reason}
    )

@given('I have a delivered order visible in order history')
def step_impl(context):
    """Pre-condition: ensure at least one order exists and is delivered via API."""
    login_res = requests.post(f"{context.base_api_url}/auth/login", json={
        "email": "root@thehundredvillages.com",
        "password": "root123"
    })
    token = login_res.json()['token']
    orders_res = requests.get(f"{context.base_api_url}/orders/", headers={"Authorization": f"Bearer {token}"})
    orders = orders_res.json()
    if orders:
        context.delivered_order_id = orders[0]['id']
        requests.put(
            f"{context.base_api_url}/orders/{orders[0]['id']}/status",
            json={"status": "Delivered"},
            headers={"Authorization": f"Bearer {token}"}
        )
    else:
        assert False, "No orders to test RMA"

@then('I should see a "Request Return" button for the delivered order')
def step_impl(context):
    from playwright.sync_api import expect
    btn = context.page.locator('button', has_text='Request Return').first
    expect(btn).to_be_visible(timeout=10000)

@when('I click "Request Return" for the delivered order')
def step_impl(context):
    btn = context.page.locator('button', has_text='Request Return').first
    btn.scroll_into_view_if_needed()
    btn.click()
    context.page.wait_for_timeout(1000)

@when('I enter return reason "{reason}" in the modal')
def step_impl(context, reason):
    textarea = context.page.locator('.modal-overlay textarea, .rma-modal textarea').first
    textarea.wait_for(state='visible', timeout=5000)
    textarea.fill(reason)

@when('I click "Submit Return Request" in the modal')
def step_impl(context):
    btn = context.page.locator('button', has_text='Submit Return Request').first
    btn.click()
    context.page.wait_for_timeout(2000)
