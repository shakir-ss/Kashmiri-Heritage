import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-123')
    
    # DATABASE CONFIG (TiDB Cloud / Secure MySQL)
    raw_db_url = os.environ.get('DATABASE_URL')
    if raw_db_url:
        # 1. Aggressively clean all whitespace/newlines
        clean_url = "".join(raw_db_url.split())
        
        # 2. Force pymysql driver for portability
        if clean_url.startswith('mysql://'):
            clean_url = clean_url.replace('mysql://', 'mysql+pymysql://', 1)
        elif clean_url.startswith('mysql+mysqldb://'):
            clean_url = clean_url.replace('mysql+mysqldb://', 'mysql+pymysql://', 1)
            
        # 3. Strip ALL query parameters to prevent driver conflicts
        if '?' in clean_url:
            clean_url = clean_url.split('?', 1)[0]
            
        SQLALCHEMY_DATABASE_URI = clean_url
        print(f"DEBUG: Database URI initialized (driver: pymysql)")
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/kashmiri_dry_fruits'
    
    # special engine options for cloud DBs
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    # Programmatic SSL Injection for ALL cloud connections
    # 'ssl': {} forces the driver to initiate SSL
    # 'ssl_verify_identity': True ensures we match the TiDB Cloud requirement
    SQLALCHEMY_ENGINE_OPTIONS["connect_args"] = {
        "ssl": {},
        "ssl_verify_identity": True 
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-456')
    
    # Twilio / WhatsApp
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
    
    # Payment Gateways
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_placeholder')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'placeholder_secret')
    STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
