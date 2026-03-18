from behave import given, when, then
from playwright.sync_api import expect

@given('I am on the Contact page')
def step_impl(context):
    context.page.goto(f"{context.base_ui_url}/contact")
    context.page.wait_for_load_state("networkidle")

@when('I fill in the contact form with:')
def step_impl(context):
    for row in context.table:
        field = row['field']
        value = row['value']
        
        if field == 'name':
            context.page.fill('input[placeholder="Your Name"]', value)
        elif field == 'email':
            context.page.fill('input[placeholder="email@example.com"]', value)
        elif field == 'phone':
            context.page.fill('input[placeholder="+91 ..."]', value)
        elif field == 'subject':
            context.page.select_option('select', label=value)
        elif field == 'message':
            context.page.fill('textarea[placeholder*="Share your thoughts"]', value)

@then('I should see the "{section_name}" section')
def step_impl(context, section_name):
    expect(context.page.locator('h2', has_text=section_name)).to_be_visible(timeout=10000)

@then('I should see an inquiry from "{name}" with subject "{subject}"')
def step_impl(context, name, subject):
    # Search in the Customer Inquiries table
    row = context.page.locator('tr', has_text=name).filter(has_text=subject)
    expect(row.first).to_be_visible(timeout=10000)
