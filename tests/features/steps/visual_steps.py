from behave import given, when, then
from playwright.sync_api import expect

@then('all images on the page should be loaded and visible')
def step_impl(context):
    # Wait for all images to finish loading (or timeout)
    context.page.wait_for_load_state("networkidle")
    
    # Optional: small extra sleep for slow CDN images
    context.page.wait_for_timeout(2000)
    
    # Find all img elements
    images = context.page.query_selector_all('img')
    
    for img in images:
        src = img.get_attribute('src')
        # Skip tiny spacer images or icons if needed, but for now check all
        
        # Check if the image is visible
        assert img.is_visible(), f"Image {src} is not visible"
        
        # Check if the image has a natural width greater than 0
        is_loaded = context.page.evaluate('''
            (img) => {
                if (!img.complete) return false;
                if (typeof img.naturalWidth === 'undefined' || img.naturalWidth === 0) return false;
                return true;
            }
        ''', img)
        
        assert is_loaded, f"Image failed to load correctly: {src}"

@then('the hero section background should be visible')
def step_impl(context):
    hero = context.page.locator('.hero')
    expect(hero).to_be_visible()
    
    # Check if the computed background-image is set
    bg_image = hero.evaluate('el => window.getComputedStyle(el).backgroundImage')
    assert bg_image != 'none', "Hero section has no background image"
    assert 'url' in bg_image, f"Hero section background image seems invalid: {bg_image}"
