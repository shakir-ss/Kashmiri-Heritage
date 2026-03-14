from flask import Blueprint, request, jsonify
from models import db, WishlistItem, Product
from .auth import token_required

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/', methods=['GET'])
@token_required
def get_wishlist(current_user):
    items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': item.id,
        'product_id': item.product_id,
        'name': item.product.name,
        'price': item.product.price,
        'image_url': item.product.image_url,
        'slug': item.product.slug
    } for item in items])

@wishlist_bp.route('/add', methods=['POST'])
@token_required
def add_to_wishlist(current_user):
    data = request.get_json()
    product_id = data.get('product_id')
    
    if not Product.query.get(product_id):
        return jsonify({'message': 'Product not found'}), 404
        
    existing = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        return jsonify({'message': 'Product already in wishlist'}), 200
        
    new_item = WishlistItem(user_id=current_user.id, product_id=product_id)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Added to wishlist'}), 201

@wishlist_bp.route('/remove/<int:product_id>', methods=['DELETE'])
@token_required
def remove_from_wishlist(current_user, product_id):
    item = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return jsonify({'message': 'Removed from wishlist'})
