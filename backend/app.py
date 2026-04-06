import threading
import time
import urllib.request
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import config_by_name
from models import db, bcrypt

def keep_alive(url):
    """Background task to self-ping the server every 14 minutes."""
    if not url:
        print("KEEP_ALIVE: No URL provided, skipping self-ping.")
        return

    print(f"KEEP_ALIVE: Starting self-ping thread for {url}")
    while True:
        try:
            time.sleep(14 * 60) # 14 minutes
            with urllib.request.urlopen(f"{url}/health") as response:
                if response.getcode() == 200:
                    print(f"KEEP_ALIVE: Ping successful at {time.ctime()}")
                else:
                    print(f"KEEP_ALIVE: Ping returned {response.getcode()} at {time.ctime()}")
        except Exception as e:
            print(f"KEEP_ALIVE ERROR: {e}")

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    CORS(app)

    # Start Keep-Alive Thread only in production
    if app.config.get('ENV') == 'production':
        render_url = os.environ.get('RENDER_EXTERNAL_URL')
        if render_url:
            threading.Thread(target=keep_alive, args=(render_url,), daemon=True).start()

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

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "message": "Welcome to The Hundred Villages API",
            "documentation": "https://github.com/shakir-ss/Kashmiri-Heritage",
            "health_check": "/health"
        }), 200

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

# Expose app at top level for Gunicorn
config_name = os.environ.get('FLASK_CONFIG', 'prod')
app = create_app(config_name)

if __name__ == "__main__":
    # Enable reloader for local development
    app.run(host='0.0.0.0', port=5000, use_reloader=True)
