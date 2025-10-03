from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from datetime import datetime
import stripe
import paypalrestsdk
import os

from models import db, User, Campaign, Donation, News, PaymentMethod
from forms import LoginForm, RegistrationForm, DonationForm, CampaignForm, NewsForm, PaymentMethodForm
from config import Config


# ----------------------------
# App Setup
# ----------------------------
app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Stripe config
stripe.api_key = app.config.get("STRIPE_SECRET_KEY", "your_stripe_secret")

# PayPal config
paypalrestsdk.configure({
    "mode": "sandbox",  # use "live" in production
    "client_id": app.config.get("PAYPAL_CLIENT_ID", "your_paypal_client_id"),
    "client_secret": app.config.get("PAYPAL_CLIENT_SECRET", "your_paypal_client_secret"),
})


# ----------------------------
# Template Helper
# ----------------------------
@app.template_global()
def moment():
    return datetime.now()


# ----------------------------
# User Loader
# ----------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------------------
# Public Routes
# ----------------------------
@app.route('/')
def index():
    campaigns = Campaign.query.filter_by(is_active=True).limit(6).all()
    news = News.query.filter_by(is_published=True).order_by(News.published_date.desc()).limit(3).all()
    return render_template('index.html', campaigns=campaigns, news=news)


# ----------------------------
# Authentication
# ----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard' if user.is_admin else 'index'))
        flash('Invalid email or password')
    return render_template('auth/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return render_template('auth/register.html', form=form)

        user = User(
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# ----------------------------
# Campaigns
# ----------------------------
@app.route('/campaigns')
def campaigns():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    query = Campaign.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    campaigns = query.paginate(page=page, per_page=9, error_out=False)
    return render_template('campaigns/index.html', campaigns=campaigns, current_category=category)


@app.route('/campaign/<int:id>')
def campaign_detail(id):
    campaign = Campaign.query.get_or_404(id)
    recent_donations = Donation.query.filter_by(
        campaign_id=id, status='confirmed', anonymous=False
    ).order_by(Donation.donation_date.desc()).limit(5).all()
    return render_template('campaigns/detail.html', campaign=campaign, recent_donations=recent_donations)


# ----------------------------
# Donations
# ----------------------------
@app.route('/donate/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def donate(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = DonationForm()
    payment_methods = PaymentMethod.query.filter_by(is_active=True).all()

    if form.validate_on_submit():
        donation = Donation(
            amount=form.amount.data,
            payment_method=form.payment_method.data,
            anonymous=form.anonymous.data,
            message=form.message.data,
            user_id=current_user.id,
            campaign_id=campaign_id
        )
        db.session.add(donation)
        db.session.commit()

        if form.payment_method.data == 'card':
            return redirect(url_for('process_stripe_payment', donation_id=donation.id))
        elif form.payment_method.data == 'paypal':
            return redirect(url_for('process_paypal_payment', donation_id=donation.id))
        else:
            return render_template('donations/manual_payment.html', donation=donation, payment_methods=payment_methods)

    return render_template('donations/donate.html', form=form, campaign=campaign, payment_methods=payment_methods)


# ----------------------------
# Payments (Stripe + PayPal)
# ----------------------------
@app.route('/process-stripe-payment/<int:donation_id>')
@login_required
def process_stripe_payment(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Donation to {donation.campaign.title}'},
                    'unit_amount': int(donation.amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('payment_success', donation_id=donation.id, _external=True),
            cancel_url=url_for('payment_cancel', donation_id=donation.id, _external=True),
        )
        donation.payment_reference = session.id
        db.session.commit()
        return redirect(session.url, code=303)
    except Exception:
        flash('Payment processing error.')
        return redirect(url_for('campaign_detail', id=donation.campaign_id))


@app.route('/payment-success/<int:donation_id>')
@login_required
def payment_success(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    donation.status = 'confirmed'
    donation.campaign.current_amount += donation.amount
    db.session.commit()
    flash('Thank you for your donation!')
    return render_template('donations/success.html', donation=donation)


@app.route('/payment-cancel/<int:donation_id>')
@login_required
def payment_cancel(donation_id):
    donation = Donation.query.get_or_404(donation_id)
    db.session.delete(donation)
    db.session.commit()
    flash('Payment cancelled.')
    return redirect(url_for('campaign_detail', id=donation.campaign_id))


# ----------------------------
# User Profile
# ----------------------------
@app.route('/profile')
@login_required
def profile():
    donations = Donation.query.filter_by(user_id=current_user.id).order_by(Donation.donation_date.desc()).all()
    return render_template('user/profile.html', donations=donations)


# ----------------------------
# News
# ----------------------------
@app.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    news_items = News.query.filter_by(is_published=True).order_by(News.published_date.desc()).paginate(page=page, per_page=6, error_out=False)
    return render_template('news/index.html', news=news_items)


@app.route('/news/<int:id>')
def news_detail(id):
    article = News.query.get_or_404(id)
    return render_template('news/detail.html', article=article)


# ----------------------------
# Static Pages
# ----------------------------
@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/contact')
def contact():
    return render_template('pages/contact.html')

@app.route('/privacy')
def privacy():
    return render_template('pages/privacy.html')


# ----------------------------
# Admin
# ----------------------------
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))

    total_campaigns = Campaign.query.count()
    total_donations = Donation.query.filter_by(status='confirmed').count()
    total_raised = db.session.query(db.func.sum(Donation.amount)).filter_by(status='confirmed').scalar() or 0
    recent_donations = Donation.query.filter_by(status='confirmed').order_by(Donation.donation_date.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           total_campaigns=total_campaigns,
                           total_donations=total_donations,
                           total_raised=total_raised,
                           recent_donations=recent_donations)


# ----------------------------
# Setup Helper
# ----------------------------
def create_tables():
    db.create_all()
    try:
        admin = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
        if not admin:
            admin = User(
                email=app.config['ADMIN_EMAIL'],
                full_name='Admin User',
                is_admin=True
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")
    except Exception as e:
        db.session.rollback()
        print(f"⚠️ Admin creation failed: {e}")


# ----------------------------
# Run
# ----------------------------
if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(host='0.0.0.0', port=5000, debug=True)
