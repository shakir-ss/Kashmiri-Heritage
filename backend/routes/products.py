from flask import Blueprint, request, jsonify
from models import db, Product, Category
from .auth import token_required, admin_required
# import slugify # We should add python-slugify to requirements later or use a simple split/replace

products_bp = Blueprint('products', __name__)

# --- CATEGORY ROUTES ---

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'slug': c.slug,
        'description': c.description
    } for c in categories])

@products_bp.route('/categories', methods=['POST'])
@token_required
@admin_required
def create_category(current_user):
    data = request.get_json()
    new_category = Category(
        name=data.get('name'),
        slug=data.get('slug') or data.get('name').lower().replace(' ', '-'),
        description=data.get('description')
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully'}), 201

# --- PRODUCT ROUTES ---

@products_bp.route('/', methods=['GET'])
def get_products():
    category_slug = request.args.get('category')
    search = request.args.get('search')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
            
    if search:
        query = query.filter(Product.name.contains(search))
        
    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'description': p.description,
        'price': p.price,
        'discount_price': p.discount_price,
        'stock': p.stock,
        'image_url': p.image_url,
        'category': p.category.name if p.category else None
    } for p in products])

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'description': product.description,
        'price': product.price,
        'discount_price': product.discount_price,
        'stock': product.stock,
        'image_url': product.image_url,
        'category_id': product.category_id
    })

@products_bp.route('/', methods=['POST'])
@token_required
@admin_required
def create_product(current_user):
    data = request.get_json()
    new_product = Product(
        name=data.get('name'),
        slug=data.get('slug') or data.get('name').lower().replace(' ', '-'),
        description=data.get('description'),
        price=data.get('price'),
        discount_price=data.get('discount_price'),
        stock=data.get('stock', 0),
        image_url=data.get('image_url'),
        category_id=data.get('category_id')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@products_bp.route('/<int:id>', methods=['PUT'])
@token_required
@admin_required
def update_product(current_user, id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.discount_price = data.get('discount_price', product.discount_price)
    product.stock = data.get('stock', product.stock)
    product.description = data.get('description', product.description)
    product.is_active = data.get('is_active', product.is_active)
    
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@products_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def delete_product(current_user, id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})
