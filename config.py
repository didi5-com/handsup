
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hands-up-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///handsup.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY') or 'pk_test_your_stripe_publishable_key'
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'sk_test_your_stripe_secret_key'
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'ikpedesire5@gmail.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'didi5566'
