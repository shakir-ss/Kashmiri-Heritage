"""
discovery_steps.py — Steps for: discovery.feature, reviews.feature
Updated to use dynamic base_api_url from environment.py
"""
from behave import given, when, then
import requests
from playwright.sync_api import expect

# ============================================================
# FACETED FILTER & SEARCH STEPS
# ============================================================

@when('I request products with min_price {min_price:d}')
def step_impl(context, min_price):
    context.response = requests.get(f"{context.base_api_url}/products/", params={"min_price": min_price})
    context.filter_min = min_price

@when('I request products with min_price {min_price:d} and max_price {max_price:d}')
def step_impl(context, min_price, max_price):
    context.response = requests.get(f"{context.base_api_url}/products/", params={
        "min_price": min_price,
        "max_price": max_price
    })
    context.filter_min = min_price
    context.filter_max = max_price

@then('all returned products should have price greater than or equal to {min_price:d}')
def step_impl(context, min_price):
    products = context.response.json()
    for p in products:
        effective_price = p.get('discount_price') or p.get('price', 0)
        assert effective_price >= min_price, \
            f"Product '{p['name']}' has price {effective_price} which is < {min_price}"

@then('all returned products should have price between {min_price:d} and {max_price:d}')
def step_impl(context, min_price, max_price):
    products = context.response.json()
    for p in products:
        effective_price = p.get('discount_price') or p.get('price', 0)
        assert min_price <= effective_price <= max_price, \
            f"Product '{p['name']}' price {effective_price} out of [{min_price}, {max_price}]"

@when('I search for products with keyword "{keyword}" using the "q" parameter')
def step_impl(context, keyword):
    context.response = requests.get(f"{context.base_api_url}/products/", params={"q": keyword})
    context.search_keyword = keyword.lower()

@then('the API should return products whose description contains "{keyword}"')
def step_impl(context, keyword):
    products = context.response.json()
    assert len(products) > 0, f"No products found for keyword '{keyword}'"
    for p in products:
        name_match = keyword.lower() in p.get('name', '').lower()
        desc_match = keyword.lower() in (p.get('description', '') or '').lower()
        details_match = keyword.lower() in (p.get('details', '') or '').lower()
        assert name_match or desc_match or details_match, \
            f"Product '{p['name']}' does not match keyword '{keyword}'"

@when('I enter min price {min_price:d} and max price {max_price:d} in the price filter')
def step_impl(context, min_price, max_price):
    min_input = context.page.locator('.price-input-wrap input').nth(0)
    max_input = context.page.locator('.price-input-wrap input').nth(1)
    min_input.fill(str(min_price))
    context.page.wait_for_timeout(400)
    max_input.fill(str(max_price))
    context.page.wait_for_timeout(500)
    context.price_min = min_price
    context.price_max = max_price

@then('the product grid should update')
def step_impl(context):
    context.page.wait_for_load_state('networkidle')
    context.page.wait_for_timeout(800)

@then('all visible products should be within the price range {min_price:d} to {max_price:d}')
def step_impl(context, min_price, max_price):
    cards = context.page.locator('.product-card').all()
    for card in cards:
        price_text = card.locator('.price').first.inner_text()
        price_num = float(price_text.replace('₹', '').replace(',', '').strip())
        assert min_price <= price_num <= max_price, \
            f"Product price ₹{price_num} is outside range [{min_price}, {max_price}]"

@when('I type "{keyword}" in the search bar')
def step_impl(context, keyword):
    search_input = context.page.locator('.search-bar input').first
    search_input.fill(keyword)
    context.page.wait_for_timeout(500)

@then('the product grid should show only products matching "{keyword}"')
def step_impl(context, keyword):
    context.page.wait_for_timeout(600)
    context.page.wait_for_load_state('networkidle')
    cards = context.page.locator('.product-card').all()
    assert len(cards) > 0, f"No products found for '{keyword}'"
    for card in cards:
        text = card.inner_text().lower()
        assert keyword.lower() in text, \
            f"Product card does not match '{keyword}': {text[:80]}"

# ============================================================
# MEGA MENU STEPS
# ============================================================

@when('I hover over the "Products" navigation link')
def step_impl(context):
    trigger = context.page.locator('.mega-trigger').first
    trigger.hover()
    context.page.wait_for_timeout(400)

@then('I should see the mega menu dropdown')
def step_impl(context):
    expect(context.page.locator('.mega-menu')).to_be_visible(timeout=5000)

@then('I should see product category cards in the mega menu')
def step_impl(context):
    cat_cards = context.page.locator('.mega-cat-card')
    expect(cat_cards.first).to_be_visible(timeout=5000)
    assert cat_cards.count() > 0, "No category cards found in mega menu"

@when('I click on a category card in the mega menu')
def step_impl(context):
    first_card = context.page.locator('.mega-cat-card').nth(1)  # skip "All Products"
    expect(first_card).to_be_visible(timeout=5000)
    first_card.click()
    context.page.wait_for_load_state('networkidle')

@then('the category filter should be applied')
def step_impl(context):
    url = context.page.url
    has_cat_param = 'category=' in url
    has_active_btn = context.page.locator('.filter-list button.active').count() > 0
    assert has_cat_param or has_active_btn, \
        f"Category filter not applied. URL: {url}"

@when('I type "{keyword}" in the mega menu search box')
def step_impl(context, keyword):
    search_input = context.page.locator('.mega-search input').first
    expect(search_input).to_be_visible(timeout=5000)
    search_input.fill(keyword)
    context.page.wait_for_timeout(400)

@then('I should see product suggestions in the mega menu dropdown')
def step_impl(context):
    suggestions = context.page.locator('.mega-suggestions .suggestion-item')
    expect(suggestions.first).to_be_visible(timeout=6000)

# ============================================================
# REVIEW STEPS
# ============================================================

@when('I submit a review for product {product_id:d} with rating {rating:d} and comment "{comment}"')
def step_impl(context, product_id, rating, comment):
    context.response = context.api_session.post(
        f"{context.base_api_url}/products/{product_id}/reviews",
        json={"rating": rating, "comment": comment}
    )

@when('I submit a review for product {product_id:d} with rating {rating:d} and comment "{comment}" without authentication')
def step_impl(context, product_id, rating, comment):
    context.response = requests.post(
        f"{context.base_api_url}/products/{product_id}/reviews",
        json={"rating": rating, "comment": comment}
    )

@when('I request product details for product {product_id:d}')
def step_impl(context, product_id):
    context.response = requests.get(f"{context.base_api_url}/products/{product_id}")

@then('the response should contain a "{field}" field')
def step_impl(context, field):
    data = context.response.json()
    assert field in data, f"Field '{field}' not found in response. Keys: {list(data.keys())}"

@then('I should see the Customer Reviews section')
def step_impl(context):
    """Check for the Customer Reviews section on the product detail page."""
    section = context.page.locator('.reviews-section, section', has_text='Customer Reviews').first
    section.scroll_into_view_if_needed()
    expect(section).to_be_visible(timeout=8000)

@then('I should see "Write a Review" form with rating selector')
def step_impl(context):
    form = context.page.locator('.review-form, .write-review')
    expect(form).to_be_visible(timeout=6000)
    rating_selector = context.page.locator('.star-rating, select[id*="rating"], .rating-select')
    expect(rating_selector.first).to_be_visible(timeout=5000)

@when('I scroll to the "Customer Reviews" section')
def step_impl(context):
    section = context.page.locator('.reviews-section, section', has_text='Customer Reviews').first
    section.scroll_into_view_if_needed()
    context.page.wait_for_timeout(800)

@when('I select rating {rating:d} in the review form')
def step_impl(context, rating):
    try:
        star = context.page.locator(f'.star-btn[data-rating="{rating}"], .star[data-value="{rating}"]').first
        star.click()
    except:
        context.page.locator('.rating-select select, select[id*="rating"]').first.select_option(str(rating))
    context.page.wait_for_timeout(300)

@when('I enter review comment "{comment}"')
def step_impl(context, comment):
    textarea = context.page.locator('.review-form textarea, .write-review textarea').first
    textarea.fill(comment)

@when('I click "Submit Review"')
def step_impl(context):
    btn = context.page.locator('button', has_text='Submit Review').first
    btn.scroll_into_view_if_needed()
    btn.click()
    context.page.wait_for_timeout(2000)

@then('I should see "{comment}" in the reviews list')
def step_impl(context, comment):
    expect(context.page.locator('body')).to_contain_text(comment, timeout=10000)

# ============================================================
# CROSS-SELL STEPS
# ============================================================

@then('I should see the You May Also Love section')
def step_impl(context):
    section = context.page.locator('.related-products').first
    section.scroll_into_view_if_needed()
    expect(section).to_be_visible(timeout=8000)

@then('I should see at least 1 related product card')
def step_impl(context):
    cards = context.page.locator('.related-card, .related-grid a')
    expect(cards.first).to_be_visible(timeout=8000)

@when('I click on the first related product in "You May Also Love"')
def step_impl(context):
    card = context.page.locator('.related-card, .related-grid a').first
    card.scroll_into_view_if_needed()
    card.click()
    context.page.wait_for_load_state('networkidle')

@then('I should be on a product detail page')
def step_impl(context):
    import re
    context.page.wait_for_url(re.compile(r".*/products/\d+"), timeout=8000)
