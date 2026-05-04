import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from behave import step, given, when, then
from backend.app import create_app
from backend.models import db, User, Category, Product, AbandonedCart, Order, Review, ReviewImage

app = create_app('dev')

@step('the latest category "{category_name}" should have image_url "{image_url}"')
def step_check_category_image(context, category_name, image_url):
    with app.app_context():
        category = Category.query.filter_by(name=category_name).order_by(Category.id.desc()).first()
        assert category is not None, f"Category {category_name} not found"
        assert category.image_url == image_url, f"Expected {image_url}, got {category.image_url}"

@step('I submit a PUT request to update the order status to "{status}" with tracking link "{tracking_link}"')
def step_update_order_tracking(context, status, tracking_link):
    order_id = context.order_id
    headers = {'Authorization': f'Bearer {context.token}'}
    data = {
        "status": status,
        "tracking_link": tracking_link,
        "tracking_number": "TRK-123"
    }
    context.response = context.api_session.put(f'{context.base_api_url}/orders/{order_id}/status', json=data, headers=headers)

@step('I track my order using the order ID and my email')
def step_track_order(context):
    order_id = context.order_id
    email = context.user_email
    context.response = context.api_session.get(f'{context.base_api_url}/orders/track?order_id={order_id}&email={email}')

@step('the JSON response should have "{key}" equal to "{value}"')
def step_check_json_key(context, key, value):
    data = context.response.json()
    assert data.get(key) == value, f"Expected {value}, got {data.get(key)}"

@step('I submit an abandoned cart payload with email "{email}"')
def step_abandoned_cart(context, email):
    data = {
        "email": email,
        "cart_data": [{"product_id": 1, "quantity": 1}]
    }
    context.response = context.api_session.post(f'{context.base_api_url}/cart/abandoned', json=data)

@step('the abandoned cart for "{email}" should exist in the database')
def step_check_abandoned_cart(context, email):
    with app.app_context():
        cart = AbandonedCart.query.filter_by(email=email).first()
        assert cart is not None

@step('I submit a POST request to "/api/reviews/" for product {product_id:d} with image "{image_url}"')
def step_submit_review_with_image(context, product_id, image_url):
    pid = getattr(context, 'test_product_id', product_id)
    with app.app_context():
        if not Product.query.get(pid):
            cat = Category.query.first() or Category(name="Test Cat", slug="test-cat")
            if not cat.id:
                db.session.add(cat)
                db.session.commit()
            prod = Product(id=pid, category_id=cat.id, name="Test Prod", slug=f"test-prod-{pid}", price=100)
            db.session.add(prod)
            db.session.commit()
    data = {
        "product_id": pid,
        "rating": 5,
        "comment": "Great!",
        "images": [image_url]
    }
    headers = {'Authorization': f'Bearer {context.token}'}
    context.response = context.api_session.post(f'{context.base_api_url}/reviews/', json=data, headers=headers)

@step('the product {product_id:d} should have a review containing image "{image_url}"')
def step_check_review_image(context, product_id, image_url):
    pid = getattr(context, 'test_product_id', product_id)
    with app.app_context():
        review = Review.query.filter_by(product_id=pid).order_by(Review.id.desc()).first()
        assert review is not None
        assert len(review.images) > 0
        assert review.images[0].image_url == image_url

@step('I am logged in as an "admin"')
def step_logged_admin(context):
    payload = {"email": "root@thehundredvillages.com", "password": "root123"}
    context.api_session.post(f"{context.base_api_url}/auth/register", json={"name": "Admin", "email": payload["email"], "password": payload["password"]})
    with app.app_context():
        u = User.query.filter_by(email=payload["email"]).first()
        if u and u.role != 'admin':
            u.role = 'admin'
            db.session.commit()
    context.response = context.api_session.post(f"{context.base_api_url}/auth/login", json=payload)
    context.token = context.response.json().get("token")
    context.api_session.headers.update({"Authorization": f"Bearer {context.token}"})

@step('I am logged in as a "customer"')
def step_logged_customer(context):
    context.api_session.post(f"{context.base_api_url}/auth/register", json={"name": "Cust", "email": "cust@test.com", "password": "pass"})
    context.response = context.api_session.post(f"{context.base_api_url}/auth/login", json={"email": "cust@test.com", "password": "pass"})
    context.token = context.response.json().get("token")
    context.api_session.headers.update({"Authorization": f"Bearer {context.token}"})
    context.user_email = "cust@test.com"

@given('I am an unauthenticated user')
def step_unauth_user(context):
    context.token = None

@step('I submit a POST request to "{endpoint}" with')
def step_post_request(context, endpoint):
    headers = {}
    if getattr(context, 'token', None):
        headers["Authorization"] = f"Bearer {context.token}"
    data = json.loads(context.text)
    context.response = context.api_session.post(f"{context.base_api_url}{endpoint.replace('/api', '')}", json=data, headers=headers)

@step('I send a GET request to "{endpoint}"')
def step_get_request(context, endpoint):
    headers = {}
    if getattr(context, 'token', None):
        headers["Authorization"] = f"Bearer {context.token}"
    context.response = context.api_session.get(f"{context.base_api_url}{endpoint.replace('/api', '')}", headers=headers)

@step('the response status code should be {code:d}')
def step_status_code(context, code):
    assert context.response.status_code == code, f"Expected {code}, got {context.response.status_code}. Response: {context.response.text}"

@step('the JSON response should contain an item with "{key}" equal to "{value}"')
def step_check_json_list(context, key, value):
    data = context.response.json()
    assert isinstance(data, list)
    assert any(item.get(key) == value for item in data)

@step('I add a product to my cart')
def step_add_cart(context):
    headers = {'Authorization': f'Bearer {context.token}'}
    with app.app_context():
        cat = Category.query.first() or Category(name="Test Cat", slug="test-cat")
        if not cat.id:
            db.session.add(cat)
            db.session.commit()
        prod = Product.query.first()
        if not prod:
            prod = Product(category_id=cat.id, name="Test Prod", slug="test-prod", price=100)
            db.session.add(prod)
            db.session.commit()
        prod_id = prod.id
        context.test_product_id = prod_id
    res = context.api_session.post(f'{context.base_api_url}/cart/add', json={"product_id": prod_id, "quantity": 1}, headers=headers)
    assert res.status_code in [200, 201], f"Add cart failed: {res.text}"

@given('I submit a POST request to "/api/orders/place" with payment mode "mock"')
def step_place_order(context):
    headers = {'Authorization': f'Bearer {context.token}'}
    data = {
        "name": "Test", "address": "Addr", "city": "City", "state": "State", 
        "country": "India", "pincode": "190001", "phone": "999", "payment_mode": "mock"
    }
    context.response = context.api_session.post(f'{context.base_api_url}/orders/place', json=data, headers=headers)

@step('I mock verify the payment for the placed order')
def step_verify_payment(context):
    order_data = context.response.json()
    context.order_id = order_data['order_id']
    headers = {'Authorization': f'Bearer {context.token}'}
    data = {
        "razorpay_order_id": order_data.get("razorpay_order_id", "mock"),
        "razorpay_payment_id": "mock_pay",
        "razorpay_signature": "mock_signature",
        "order_id": context.order_id
    }
    context.response = context.api_session.post(f'{context.base_api_url}/orders/verify', json=data, headers=headers)

@step('my order is created and status is "paid"')
def step_check_paid(context):
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}. Body: {context.response.text}"
    with app.app_context():
        order = Order.query.get(context.order_id)
        assert order.status in ["paid", "processing"], f"Expected paid/processing, got {order.status}"
