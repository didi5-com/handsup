
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hands-up-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///handsup.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'ikpedesire5@gmail.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'didi5566'
