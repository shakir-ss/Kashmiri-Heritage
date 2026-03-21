from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import config_by_name
from models import db, bcrypt

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    CORS(app)

    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.cart import cart_bp
    from routes.orders import orders_bp
    from routes.analytics import analytics_bp
    from routes.wishlist import wishlist_bp
    from routes.contact import contact_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(wishlist_bp, url_prefix='/api/wishlist')
    app.register_blueprint(contact_bp, url_prefix='/api/contact')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "The Hundred Villages API"}), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    import os
    config_name = os.environ.get('FLASK_CONFIG', 'dev')
    app = create_app(config_name)
    app.run(host='0.0.0.0', port=5000, use_reloader=False)
