from flask import Blueprint, request, jsonify, current_app
from models import db, Order, OrderItem, CartItem, Product, User
from .auth import token_required, admin_required
from services.messaging_service import MessagingService

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/admin', methods=['GET'])
@token_required
@admin_required
def admin_get_all_orders(current_user):
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id': o.id,
        'customer_name': o.user.name,
        'customer_email': o.user.email,
        'total_amount': o.total_amount,
        'status': o.status,
        'address': o.address,
        'phone': o.phone,
        'created_at': o.created_at,
        'items': [{
            'name': item.product.name,
            'quantity': item.quantity,
            'price': item.price_at_purchase
        } for item in o.items]
    } for o in orders])

@orders_bp.route('/place', methods=['POST'])
@token_required
def place_order(current_user):
    data = request.get_json()
    print(f"DEBUG PLACE ORDER DATA: {data}")
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        print("DEBUG: Cart is empty for user", current_user.id)
        return jsonify({'message': 'Cart is empty'}), 400

    address = data.get('address', '')
    pincode = data.get('pincode', '')
    payment_mode = data.get('payment_mode', 'upi')
    
    # Specific Local Pincodes List
    LOCAL_PINCODES = ['190001', '190002', '190003', '190004', '190005', '190006', '190007', '190008', '190009', '190010']
    
    delivery_charge = 0
    if pincode not in LOCAL_PINCODES:
        delivery_charge = 50.0

    # Calculate subtotal
    subtotal = 0
    order_items_to_create = []
    
    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            return jsonify({'message': f'Not enough stock for {product.name}'}), 400
        
        price = product.discount_price or product.price
        subtotal += price * item.quantity
        
        # Deduct stock
        product.stock -= item.quantity
        
        order_items_to_create.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=price
        ))

    total_amount = subtotal + delivery_charge
    prepaid_amount = total_amount
    balance_on_delivery = 0.0

    # Handle Partial COD (30/70 rule)
    if payment_mode == 'cod':
        prepaid_amount = total_amount * 0.30
        balance_on_delivery = total_amount * 0.70

    # Create Order
    new_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        prepaid_amount=prepaid_amount,
        balance_on_delivery=balance_on_delivery,
        status='paid' if payment_mode != 'cod' else 'partial_paid',
        address=f"{address} (PIN: {pincode})",
        phone=data.get('phone'),
        payment_id=data.get('payment_id', 'MOCK_PAYMENT_ID')
    )

    db.session.add(new_order)
    db.session.flush() # Get order ID

    for oi in order_items_to_create:
        oi.order_id = new_order.id
        db.session.add(oi)

    # Clear Cart
    CartItem.query.filter_by(user_id=current_user.id).delete()
    
    db.session.commit()

    # Trigger WhatsApp (Async via threading)
    import threading
    def notify():
        try:
            with current_app.app_context():
                MessagingService.send_order_confirmation(new_order.phone, new_order.id, total_amount)
        except Exception as e:
            print(f"Async WhatsApp notification failed: {e}")
    
    threading.Thread(target=notify).start()

    return jsonify({
        'message': 'Order placed successfully',
        'order_id': new_order.id
    }), 201

@orders_bp.route('/', methods=['GET'])
@token_required
def get_user_orders(current_user):
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': o.id,
        'total_amount': o.total_amount,
        'status': o.status,
        'created_at': o.created_at,
        'items': [{
            'name': item.product.name,
            'quantity': item.quantity,
            'price': item.price_at_purchase
        } for item in o.items]
    } for o in orders])
