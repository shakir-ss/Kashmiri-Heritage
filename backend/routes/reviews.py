from flask import Blueprint, request, jsonify
from models import db, Review, ReviewImage

reviews_bp = Blueprint('reviews_bp', __name__)

@reviews_bp.route('/', methods=['POST'])
def add_review():
    data = request.json
    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = data.get('comment', '')
    image_urls = data.get('images', [])
    user_id = data.get('user_id') # Optional for guest

    if not product_id or not rating:
        return jsonify({"message": "Product ID and rating are required"}), 400

    review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()

    for url in image_urls:
        review_image = ReviewImage(review_id=review.id, image_url=url)
        db.session.add(review_image)
    
    db.session.commit()

    return jsonify({"message": "Review submitted successfully"}), 201

@reviews_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id, is_approved=True).all()
    results = []
    for r in reviews:
        images = [img.image_url for img in r.images]
        results.append({
            "id": r.id,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at,
            "images": images,
            "user": "Verified Buyer" # Could map to user_id later
        })
    return jsonify(results), 200
