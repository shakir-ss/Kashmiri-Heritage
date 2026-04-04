import threading
import razorpay
import time
from flask import Blueprint, request, jsonify, current_app
from models import db, Order, OrderItem, CartItem, Product, User
from .auth import token_required, admin_required
from services.messaging_service import MessagingService

orders_bp = Blueprint('orders', __name__)

# Initialize Razorpay Client (Using keys from config/env)
def get_razorpay_client():
    return razorpay.Client(auth=(
        current_app.config.get('RAZORPAY_KEY_ID'),
        current_app.config.get('RAZORPAY_KEY_SECRET')
    ))

@orders_bp.route('/place', methods=['POST'])
@token_required
def place_order(current_user):
    data = request.get_json()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

    address = data.get('address', '')
    pincode = data.get('pincode', '')
    payment_mode = data.get('payment_mode', 'upi')
    
    LOCAL_PINCODES = ['190001', '190002', '190003', '190004', '190005', '190006', '190007', '190008', '190009', '190010']
    
    delivery_charge = 0
    if pincode not in LOCAL_PINCODES:
        delivery_charge = 50.0

    subtotal = 0
    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            return jsonify({'message': f'Not enough stock for {product.name}'}), 400
        subtotal += (product.discount_price or product.price) * item.quantity

    total_amount = subtotal + delivery_charge
    
    # Calculate amount to pay NOW (Full for UPI/Card, 30% for COD)
    amount_to_pay = total_amount
    if payment_mode == 'cod':
        amount_to_pay = total_amount * 0.30

    # 1. Create Razorpay Order (The "Handshake" starts here)
    razorpay_order_id = "mock_order_" + str(int(time.time()))
    if payment_mode == 'mock':
        if not current_app.config.get('ENABLE_MOCK_PAYMENT'):
            return jsonify({'message': 'Mock payment is not enabled in this environment'}), 403
        print("DEBUG: Bypassing Razorpay Order creation for Mock Payment.")
    else:
        try:
            client = get_razorpay_client()
            razorpay_order = client.order.create({
                "amount": int(amount_to_pay * 100), # Amount in paise (100 paise = 1 INR)
                "currency": "INR",
                "payment_capture": "1" # Auto-capture
            })
            razorpay_order_id = razorpay_order['id']
        except Exception as e:
            print(f"RAZORPAY ERROR: {e}")
            return jsonify({'message': 'Payment gateway unavailable'}), 503

    # Create local Order record (Status: pending)
    new_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        prepaid_amount=amount_to_pay,
        balance_on_delivery=total_amount - amount_to_pay if payment_mode == 'cod' else 0,
        status='pending',
        address=address,
        city=data.get('city'),
        state=data.get('state'),
        country=data.get('country', 'India'),
        pincode=pincode,
        phone=data.get('phone'),
        payment_id=razorpay_order_id # Store RZP Order ID temporarily
    )

    db.session.add(new_order)
    db.session.flush()

    for item in cart_items:
        price = item.product.discount_price or item.product.price
        db.session.add(OrderItem(
            order_id=new_order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price_at_purchase=price
        ))
        # Optional: Reserve stock (Don't deduct fully yet until payment verified)

    db.session.commit()

    return jsonify({
        'message': 'Handshake initiated',
        'razorpay_order_id': razorpay_order_id,
        'order_id': new_order.id,
        'amount': amount_to_pay,
        'key': current_app.config.get('RAZORPAY_KEY_ID')
    }), 201

@orders_bp.route('/verify', methods=['POST'])
@token_required
def verify_payment(current_user):
    data = request.get_json()
    
    # QA Mock Bypass
    is_mock = False
    if data.get('razorpay_signature') == 'mock_signature':
        if current_app.config.get('ENABLE_MOCK_PAYMENT') and current_app.config.get('ENV') != 'production':
            is_mock = True
        else:
            return jsonify({'message': 'Mock signature detected but mock payments are disabled or in production'}), 403

    if is_mock:
        try:
            order_id = int(data.get('order_id'))
            order = Order.query.get(order_id)
            if order and order.user_id == current_user.id:
                order.status = 'paid' if order.balance_on_delivery == 0 else 'partial_paid'
                order.payment_id = data.get('razorpay_payment_id') or "mock_id"
                CartItem.query.filter_by(user_id=current_user.id).delete()
                db.session.commit()
                return jsonify({'message': 'Mock Verified', 'order_id': order.id}), 200
            
            error_msg = f"Mock Check Failed: OrderFound={order is not None}"
            if order: error_msg += f", OrderUID={order.user_id}, CurrentUID={current_user.id}"
            return jsonify({'message': error_msg}), 400
        except Exception as e:
            return jsonify({'message': f"Mock Exception: {str(e)}"}), 400

    try:
        client = get_razorpay_client()
        client.utility.verify_payment_signature({
            'razorpay_order_id': data.get('razorpay_order_id'),
            'razorpay_payment_id': data.get('razorpay_payment_id'),
            'razorpay_signature': data.get('razorpay_signature')
        })
        
        order_id = data.get('order_id')
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({'message': 'Order not found'}), 404
            
        if order.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403

        order.status = 'paid' if order.balance_on_delivery == 0 else 'partial_paid'
        order.payment_id = data.get('razorpay_payment_id')

        # Deduct stock
        for item in order.items:
            item.product.stock -= item.quantity

        # Clear Cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        # WhatsApp (only for real payments)
        def notify():
            try:
                with current_app.app_context():
                    MessagingService.send_order_confirmation(order.phone, order.id, order.total_amount)
            except: pass
        threading.Thread(target=notify).start()

        return jsonify({'message': 'Verified', 'order_id': order.id}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 400

@orders_bp.route('/', methods=['GET'])
@token_required
def get_user_orders(current_user):
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
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

@orders_bp.route('/admin', methods=['GET'])
@token_required
@admin_required
def get_all_orders(current_user):
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id': o.id,
        'user': o.user.name,
        'user_email': o.user.email,
        'total_amount': o.total_amount,
        'prepaid_amount': o.prepaid_amount,
        'balance_on_delivery': o.balance_on_delivery,
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

@orders_bp.route('/<int:id>/status', methods=['PUT'])
@token_required
@admin_required
def update_order_status(current_user, id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    status = data.get('status')
    if status:
        order.status = status
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully'})
    return jsonify({'message': 'Status is required'}), 400
