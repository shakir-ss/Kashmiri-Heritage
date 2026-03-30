import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-123')
    
    # DATABASE CONFIG (TiDB Cloud / Secure MySQL)
    # Aggressively remove all whitespace/newlines from the URL
    raw_db_url = os.environ.get('DATABASE_URL')
    if raw_db_url:
        SQLALCHEMY_DATABASE_URI = "".join(raw_db_url.split())
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/kashmiri_dry_fruits'
    
    # Special engine options for secure cloud connections
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    # If the database URL contains SSL parameters, they will be parsed automatically
    # but we ensure the dialect is correct if using pymysql
    if SQLALCHEMY_DATABASE_URI.startswith('mysql://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('mysql://', 'mysql+pymysql://', 1)
    elif SQLALCHEMY_DATABASE_URI.startswith('mysql+mysqldb://'):
        # For Render/Vercel, pymysql is often more portable than mysqlclient
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('mysql+mysqldb://', 'mysql+pymysql://', 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-456')
    
    # Twilio / WhatsApp
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
    
    # Payment Gateways
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_KRKbOD0PJbYKoB')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', '3vcmj8AmebbfOqbDAMbhmjon')
    STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
