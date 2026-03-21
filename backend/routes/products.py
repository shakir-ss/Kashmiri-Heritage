from flask import Blueprint, request, jsonify
from models import db, Product, Category, ProductImage, ProductVariant
from .auth import token_required, admin_required

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
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Category name is required'}), 400
        
    slug = data.get('slug') or name.lower().replace(' ', '-')
    
    # Check if slug exists and make it unique
    base_slug = slug
    counter = 1
    while Category.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    new_category = Category(
        name=name,
        slug=slug,
        description=data.get('description')
    )
    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Category created successfully', 'id': new_category.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating category: {str(e)}'}), 500

@products_bp.route('/categories/<int:id>', methods=['PUT'])
@token_required
@admin_required
def update_category(current_user, id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    name = data.get('name', category.name)
    category.name = name
    category.description = data.get('description', category.description)
    
    slug = data.get('slug') or name.lower().replace(' ', '-')
    
    # Unique slug check excluding self
    base_slug = slug
    counter = 1
    while Category.query.filter(Category.slug == slug, Category.id != id).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
        
    category.slug = slug
    try:
        db.session.commit()
        return jsonify({'message': 'Category updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating category: {str(e)}'}), 500

@products_bp.route('/categories/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def delete_category(current_user, id):
    category = Category.query.get_or_404(id)
    # Check if category has products
    if category.products:
        return jsonify({'message': 'Cannot delete category with associated products'}), 400
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})

# --- PRODUCT ROUTES ---

@products_bp.route('/', methods=['GET'])
def get_products():
    category_param = request.args.get('category')
    search = request.args.get('search')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_param:
        # Check if it's an ID (numeric) or a slug
        if category_param.isdigit():
            query = query.filter_by(category_id=int(category_param))
        else:
            category = Category.query.filter_by(slug=category_param).first()
            if category:
                query = query.filter_by(category_id=category.id)
            else:
                # If slug not found, return empty list or ignore filter
                # For now, let's just make the query return nothing to be strict
                query = query.filter(Product.id == -1)
            
    if search:
        query = query.filter(Product.name.contains(search))
        
    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'description': p.description,
        'details': p.details,
        'price': p.price,
        'discount_price': p.discount_price,
        'stock': p.stock,
        'image_url': p.image_url,
        'category': p.category.name if p.category else None,
        'category_id': p.category_id,
        'images': [img.image_url for img in p.images],
        'weight_grams': p.weight_grams,
        'attributes': p.attributes,
        'variants': [{
            'id': v.id,
            'name': v.name,
            'price_modifier': v.price_modifier,
            'stock': v.stock,
            'sku': v.sku
        } for v in p.variants]
    } for p in products])

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'description': product.description,
        'details': product.details,
        'price': product.price,
        'discount_price': product.discount_price,
        'stock': product.stock,
        'image_url': product.image_url,
        'category_id': product.category_id,
        'images': [img.image_url for img in product.images],
        'weight_grams': product.weight_grams,
        'attributes': product.attributes,
        'variants': [{
            'id': v.id,
            'name': v.name,
            'price_modifier': v.price_modifier,
            'stock': v.stock,
            'sku': v.sku
        } for v in product.variants]
    })

@products_bp.route('/', methods=['POST'])
@token_required
@admin_required
def create_product(current_user):
    data = request.get_json()
    name = data.get('name')
    slug = data.get('slug') or name.lower().replace(' ', '-')
    
    # Unique slug check
    base_slug = slug
    counter = 1
    while Product.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    new_product = Product(
        name=name,
        slug=slug,
        description=data.get('description'),
        details=data.get('details'),
        price=data.get('price'),
        discount_price=data.get('discount_price'),
        stock=data.get('stock', 0),
        image_url=data.get('image_url'),
        category_id=data.get('category_id'),
        weight_grams=data.get('weight_grams', 0),
        attributes=data.get('attributes', {})
    )
    
    # Handle additional images
    additional_images = data.get('additional_images', [])
    for url in additional_images:
        if url:
            new_product.images.append(ProductImage(image_url=url))

    # Handle variants
    variants_data = data.get('variants', [])
    for v in variants_data:
        if v.get('name'):
            sku = v.get('sku')
            if not sku:
                import random
                sku = f"SKU-{random.randint(100000, 999999)}"
            
            new_product.variants.append(ProductVariant(
                name=v['name'],
                price_modifier=v.get('price_modifier', 0.0),
                stock=v.get('stock', 0),
                sku=sku
            ))

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
    product.details = data.get('details', product.details)
    product.is_active = data.get('is_active', product.is_active)
    product.image_url = data.get('image_url', product.image_url)
    product.category_id = data.get('category_id', product.category_id)
    product.weight_grams = data.get('weight_grams', product.weight_grams)
    product.attributes = data.get('attributes', product.attributes)
    
    # Update additional images
    if 'additional_images' in data:
        # Clear existing images
        ProductImage.query.filter_by(product_id=id).delete()
        # Add new ones
        for url in data.get('additional_images', []):
            if url:
                db.session.add(ProductImage(product_id=id, image_url=url))

    # Update variants
    if 'variants' in data:
        ProductVariant.query.filter_by(product_id=id).delete()
        for v in data.get('variants', []):
            if v.get('name'):
                db.session.add(ProductVariant(
                    product_id=id,
                    name=v['name'],
                    price_modifier=v.get('price_modifier', 0.0),
                    stock=v.get('stock', 0),
                    sku=v.get('sku')
                ))
    
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
