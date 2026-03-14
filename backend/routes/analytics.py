from flask import Blueprint, jsonify
from models import db, Analytics, Product, Order, OrderItem, CartItem
from .auth import token_required, admin_required
from datetime import datetime, timedelta
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/view/<int:product_id>', methods=['POST'])
def record_view(product_id):
    """Increments the view count for a specific product."""
    stat = Analytics.query.filter_by(product_id=product_id).first()
    if not stat:
        stat = Analytics(product_id=product_id, view_count=1)
        db.session.add(stat)
    else:
        stat.view_count += 1
        stat.last_viewed_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'message': 'View recorded'}), 200

@analytics_bp.route('/stats', methods=['GET'])
@token_required
@admin_required
def get_stats(current_user):
    """Returns key business metrics for the admin dashboard."""
    
    # 1. Total Revenue (Paid Orders)
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter(Order.status == 'paid').scalar() or 0
    
    # 2. Total Orders
    total_orders = Order.query.filter_by(status='paid').count()
    
    # 3. Popular Products (by View Count)
    popular_products = db.session.query(
        Product.name, Analytics.view_count
    ).join(Analytics).order_by(Analytics.view_count.desc()).limit(5).all()
    
    # 4. Best Sellers (by Quantity Sold)
    best_sellers = db.session.query(
        Product.name, func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).group_by(Product.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
    
    # 5. Abandoned Carts (Carts older than 24 hours)
    yesterday = datetime.utcnow() - timedelta(hours=24)
    abandoned_carts_count = db.session.query(func.count(func.distinct(CartItem.user_id)))\
        .filter(CartItem.updated_at < yesterday).scalar() or 0

    return jsonify({
        'revenue': round(total_revenue, 2),
        'total_orders': total_orders,
        'popular_items': [{'name': p[0], 'views': p[1]} for p in popular_products],
        'best_sellers': [{'name': p[0], 'sold': int(p[1])} for p in best_sellers],
        'abandoned_carts': abandoned_carts_count
    }), 200
