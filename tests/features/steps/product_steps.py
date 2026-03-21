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
    unique_name = f"{name} {random.randint(1000, 9999)}"
    payload = {
        "name": unique_name,
        "price": float(price),
        "stock": stock,
        "category_id": cat_id,
        "image_url": None
    }
    context.response = context.api_session.post(f"{context.base_api_url}/products/", json=payload)

# --- UI STEPS ---

@when('I try to create a product without an auth token')
def step_impl(context):
    payload = {
        "name": "Unauthorized Item",
        "price": 100,
        "stock": 10,
        "category_id": 1
    }
    # Send request without Authorization header
    context.response = requests.post(f"{context.base_api_url}/products/", json=payload)

@then('the API should return an error message "{message}"')
def step_impl(context, message):
    data = context.response.json()
    assert data.get('message') == message

@given('I create a product with name "{name}", price {price:d}, stock {stock:d}, and details "{details}"')
def step_impl(context, name, price, stock, details):
    cat_id = getattr(context, 'valid_cat_id', 1)
    unique_name = f"{name} {random.randint(1000, 9999)}"
    # Store unique name in context for later steps
    context.last_product_name = unique_name
    payload = {
        "name": unique_name,
        "price": float(price),
        "stock": stock,
        "category_id": cat_id,
        "details": details
    }
    
    headers = {}
    if hasattr(context, 'token'):
        headers['Authorization'] = f"Bearer {context.token}"
        
    context.response = context.api_session.post(
        f"{context.base_api_url}/products/", 
        json=payload,
        headers=headers
    )
    assert context.response.status_code == 201, f"Expected 201 but got {context.response.status_code}: {context.response.text}"

@given('I am on the Products page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/products")

@then('I should see product "{name}"')
def step_impl(context, name):
    # Use context.last_product_name if name matches placeholder
    actual_name = context.last_product_name if name == "Limited Edition Box" or name == "Multi-Pack Saffron" or name == "Local Image Product" else name
    expect(context.page.get_by_text(actual_name).first).to_be_visible()

@then('product "{name}" should show "{status}" or "{alt_status}"')
def step_impl(context, name, status, alt_status):
    actual_name = context.last_product_name if name == "Limited Edition Box" else name
    card = context.page.locator('.product-card', has_text=actual_name).first
    expect(card).to_contain_text(re.compile(f"{status}|{alt_status}"))

@when('I click on the "{name}" category card')
def step_impl(context, name):
    # Find the category card by name and click the 'View All' link inside it
    card = context.page.locator('.category-card', has_text=name).first
    card.locator('.btn-link').click()

@then('the "{name}" category should be active in the sidebar')
def step_impl(context, name):
    # Check for the active button in the sidebar filter list
    active_btn = context.page.locator('.filter-list button.active')
    expect(active_btn).to_have_text(name)

@then('I should be on the Products page')
def step_impl(context):
    expect(context.page).to_have_url(re.compile(r".*/products(\?.*)?$"))
    expect(context.page.locator('h3', has_text="Categories")).to_be_visible()

@then('I should see the product detail page for "{name}"')
def step_impl(context, name):
    actual_name = context.last_product_name if name == "Limited Edition Box" or name == "Multi-Pack Saffron" or name == "Local Image Product" else name
    expect(context.page.locator('h1')).to_contain_text(actual_name)
    expect(context.page).to_have_url(re.compile(r".*/products/\d+"))

@then('product "{name}" should show "{status}"')
def step_impl(context, name, status):
    actual_name = context.last_product_name if name == "Limited Edition Box" else name
    card = context.page.locator('.product-card', has_text=actual_name).first
    expect(card).to_contain_text(status)

@then('I should see a list of products')
def step_impl(context):
    # Wait for product cards to load
    context.page.wait_for_selector('.product-card')
    cards = context.page.locator('.product-card')
    assert cards.count() > 0

@then('I should see the product story "{text}"')
def step_impl(context, text):
    expect(context.page.locator('.details-content')).to_contain_text(text)

@when('I fill in the product form with name "{name}", price {price:d}, stock {stock:d}, and details "{details}"')
@given('I fill in the product form with name "{name}", price {price:d}, stock {stock:d}, and details "{details}"')
def step_impl(context, name, price, stock, details):
    # Generate unique name ONLY if not already in context
    if not hasattr(context, 'last_product_name'):
        unique_name = f"{name} {random.randint(1000, 9999)}"
        context.last_product_name = unique_name
    else:
        unique_name = context.last_product_name
    
    # Open the add modal first
    context.page.click('#add-product-btn')
    
    # Wait for modal content
    try:
        context.page.wait_for_selector('.modal-content', state='visible', timeout=5000)
        
        # Fill based on labels or IDs
        context.page.get_by_label("Product Name").fill(unique_name)
        context.page.get_by_label("Base Price (₹)").fill(str(price))
        context.page.get_by_label("Total Stock").fill(str(stock))
        # Select category - assuming first option
        context.page.get_by_label("Category").select_option(index=1)
        context.page.get_by_label("Detailed Product Story").fill(details)
        context.page.get_by_label("Main Image URL").fill("https://via.placeholder.com/600x800?text=Main+Image")
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

@when('I add an additional image URL "{url}"')
def step_impl(context, url):
    context.page.get_by_text("+ Add Another Image").click()
    # Fill the last input in the image-input-row list
    context.page.locator('.image-input-row input').last.fill(url)

@then('I should see {count:d} images in the gallery')
def step_impl(context, count):
    # Main image + thumbnails
    thumbnails = context.page.locator('.thumb-card')
    expect(thumbnails).to_have_count(count)

@when('I click "+ New Category"')
@given('I click "+ New Category"')
def step_impl(context):
    context.page.get_by_text("+ New Category").click()

@when('I fill in category name "{name}" and description "{description}"')
@given('I fill in category name "{name}" and description "{description}"')
def step_impl(context, name, description):
    context.page.get_by_label("Category Name").fill(name)
    context.page.get_by_label("Description").fill(description)

@then('I should see the category "{name}" in the category list')
def step_impl(context, name):
    expect(context.page.locator('table.admin-table').filter(has_text="Slug")).to_contain_text(name)

@then('I should see the product "{name}" in the product list')
def step_impl(context, name):
    # Use unique name if applicable
    actual_name = context.last_product_name if name == "Multi-Pack Saffron" or name == "Local Image Product" else name
    # Check the specific admin table for products, not orders
    try:
        product_table = context.page.locator('table.admin-table').filter(has_text="Product").first
        expect(product_table).to_contain_text(actual_name, timeout=10000)
    except Exception as e:
        context.page.screenshot(path="error_product_list.png")
        raise e

@when('I click on product "{name}"')
def step_impl(context, name):
    # Use unique name if applicable
    actual_name = getattr(context, 'last_product_name', name) if name in ["Multi-Pack Saffron", "Local Image Product", "Kashmiri Kahwa Set"] else name
    # Find the product card by name and click the link or the card itself
    card = context.page.locator('.product-card', has_text=actual_name).first
    card.click()

@when('I edit the category "{name}" to name "{new_name}"')
def step_impl(context, name, new_name):
    # Find the row with category name and click Edit
    row = context.page.locator('tr', has_text=name).first
    row.get_by_text("Edit").click()
    context.page.get_by_label("Category Name").fill(new_name)

@then('the "Add to Cart" button for "{name}" should be disabled')
def step_impl(context, name):
    actual_name = context.last_product_name if name == "Limited Edition Box" else name
    card = context.page.locator('.product-card', has_text=actual_name).first
    btn = card.locator('button:has-text("Out of Stock")')
    expect(btn).to_be_disabled()

@when('I add {count:d} items to the cart')
def step_impl(context, count):
    # Wait for the quantity selector to be visible
    context.page.wait_for_selector('.quantity-selector')
    # If count > 1, click + button (count - 1) times
    for _ in range(count - 1):
        context.page.locator('.quantity-selector button').filter(has_text="+").click()
    
    # Click Add to Cart
    context.page.get_by_role("button", name="Add to Cart").click()

@when('I click id "{element_id}"')
def step_impl(context, element_id):
    context.page.click(f"#{element_id}")

@when('I fill in "{label}" with "{value}"')
@given('I fill in "{label}" with "{value}"')
def step_impl(context, label, value):
    if label == "Product Name":
        unique_name = f"{value} {random.randint(1000, 9999)}"
        context.last_product_name = unique_name
        context.page.get_by_label(label).fill(unique_name)
    elif label == "Full Name":
        context.page.locator('input[id="full-name"]').fill(value)
    elif label == "Phone Number":
        context.page.locator('input[id="phone"]').fill(value)
    elif label == "Shipping Address":
        context.page.locator('input[id="address"]').fill(value)
    elif label == "City":
        context.page.locator('input[id="city"]').fill(value)
    elif label == "Area Pincode" or label == "Pincode":
        context.page.wait_for_selector('input[id="pincode"]', state='visible', timeout=10000)
        context.page.locator('input[id="pincode"]').fill(value)
    else:
        context.page.get_by_label(label).fill(value)

@then('product "{name}" should have image source starting with "{path_prefix}"')
def step_impl(context, name, path_prefix):
    actual_name = context.last_product_name if name == "Local Image Product" else name
    card = context.page.locator('.product-card', has_text=actual_name).first
    img = card.locator('img')
    src = img.get_attribute('src')
    # If using dev server, it might be http://localhost:3000/images/...
    assert path_prefix in src, f"Expected {path_prefix} in {src}"

@when('I fill in variant {idx:d} name "{name}", modifier {modifier:d}, and stock {stock:d}')
@given('I fill in variant {idx:d} name "{name}", modifier {modifier:d}, and stock {stock:d}')
def step_impl(context, idx, name, modifier, stock):
    # variant-input-row list
    row = context.page.locator('.variant-input-row').nth(idx-1)
    row.locator('input[placeholder*="Variant Name"]').fill(name)
    row.locator('input[placeholder="+₹"]').fill(str(modifier))
    row.locator('input[placeholder="Stock"]').fill(str(stock))

@when('I select category "{name}"')
@given('I select category "{name}"')
def step_impl(context, name):
    context.page.get_by_label("Category").select_option(label=name)

@when('I click button "{text}"')
@given('I click button "{text}"')
def step_impl(context, text):
    # Try getting by role button first, then general text
    try:
        btn = context.page.get_by_role("button", name=text, exact=True)
        if btn.count() > 0:
            btn.first.click()
        else:
            context.page.get_by_text(text, exact=True).first.click()
    except:
        # Fallback to locator with has-text
        context.page.locator(f":has-text('{text}')").first.click()

@then('I should see the variant chip "{name}"')
def step_impl(context, name):
    expect(context.page.locator('.variant-chip', has_text=name).first).to_be_visible()

@when('I click variant chip "{name}"')
def step_impl(context, name):
    context.page.locator('.variant-chip', has_text=name).first.click()

@then('the price should show "{price}"')
def step_impl(context, price):
    expect(context.page.locator('.current-price')).to_contain_text(price)

@then('I should see the Heritage Section with label "{label}" and title "{title}"')
def step_impl(context, label, title):
    heritage_section = context.page.locator('.artisan-heritage')
    expect(heritage_section.locator('.heritage-label')).to_have_text(label)
    expect(heritage_section.locator('h2')).to_have_text(title)

@when('I click the modal button "{button_text}"')
@given('I click the modal button "{button_text}"')
@then('I click the modal button "{button_text}"')
def step_impl(context, button_text):
    # Try multiple ways to find the button
    try:
        # 1. Direct text match
        btn = context.page.get_by_role("button", name=button_text, exact=True)
        if btn.count() > 0:
            btn.first.click()
        else:
            # 2. Contains text
            btn = context.page.locator(f'button:has-text("{button_text}")').first
            btn.click()
            
        # If it's a save/submit button, wait for modal to disappear
        if "Proceed to Checkout" in button_text:
            context.page.wait_for_load_state("networkidle")
            context.page.wait_for_timeout(3000)
        elif "Save" in button_text or "Pay" in button_text:
            context.page.wait_for_selector('.modal-overlay', state='hidden', timeout=10000)
            
    except Exception as e:
        context.page.screenshot(path=f"error_modal_btn_{button_text.replace(' ', '_')}.png")
        raise e
