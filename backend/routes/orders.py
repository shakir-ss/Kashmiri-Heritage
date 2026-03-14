from flask import Blueprint, request, jsonify
from models import db, Order, OrderItem, CartItem, Product
from .auth import token_required
from services.messaging_service import MessagingService

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/place', methods=['POST'])
@token_required
def place_order(current_user):
    data = request.get_json()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

    # Calculate total and validate stock
    total_amount = 0
    order_items_to_create = []
    
    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            return jsonify({'message': f'Not enough stock for {product.name}'}), 400
        
        price = product.discount_price or product.price
        total_amount += price * item.quantity
        
        # Deduct stock
        product.stock -= item.quantity
        
        order_items_to_create.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=price
        ))

    # Create Order
    new_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status='paid', # Mocking immediate payment for prototype
        address=data.get('address'),
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

    # Trigger WhatsApp (Async ideally, but sync for now)
    MessagingService.send_order_confirmation(new_order.phone, new_order.id, total_amount)

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
