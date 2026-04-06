from flask import Blueprint, request, jsonify
from models import db, CartItem, Product
from .auth import token_required

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@token_required
def get_cart(current_user):
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': item.id,
        'product_id': item.product_id,
        'name': item.product.name,
        'price': item.product.discount_price or item.product.price,
        'quantity': item.quantity,
        'image_url': item.product.image_url,
        'stock': item.product.stock  # Crucial: Send real-time stock
    } for item in items])

@cart_bp.route('/add', methods=['POST'])
@token_required
def add_to_cart(current_user):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    # Explicit check for product existence
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(item)
    
    db.session.commit()
    return jsonify({'message': 'Item added to cart'}), 201

@cart_bp.route('/update', methods=['PUT'])
@token_required
def update_cart(current_user):
    data = request.get_json()
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=data.get('product_id')).first()
    if item:
        item.quantity = data.get('quantity')
        if item.quantity <= 0:
            db.session.delete(item)
        db.session.commit()
    return jsonify({'message': 'Cart updated'})

@cart_bp.route('/<int:product_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user, product_id):
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return jsonify({'message': 'Item removed from cart'})

@cart_bp.route('/clear', methods=['DELETE'])
@token_required
def clear_cart(current_user):
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'message': 'Cart cleared'})
