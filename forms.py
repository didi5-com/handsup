
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])

class DonationForm(FlaskForm):
    amount = FloatField('Donation Amount', validators=[DataRequired(), NumberRange(min=1)])
    payment_method = SelectField('Payment Method', 
                               choices=[('card', 'Credit/Debit Card'),
                                       ('paypal', 'PayPal'),
                                       ('crypto', 'Cryptocurrency'), 
                                       ('bank', 'Bank Transfer')])
    anonymous = BooleanField('Donate Anonymously')
    message = TextAreaField('Message (Optional)', widget=TextArea())

class CampaignForm(FlaskForm):
    title = StringField('Campaign Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=50)])
    goal_amount = FloatField('Goal Amount', validators=[DataRequired(), NumberRange(min=100)])
    category = SelectField('Category', 
                         choices=[('', 'Select Category'),
                                 ('health', 'Health'),
                                 ('education', 'Education'), 
                                 ('environment', 'Environment'),
                                 ('emergency', 'Emergency Relief'),
                                 ('community', 'Community'),
                                 ('animals', 'Animals')])
    image_url = StringField('Image URL', validators=[Length(max=300)])
    end_date = DateField('End Date (Optional)', format='%Y-%m-%d')

class NewsForm(FlaskForm):
    title = StringField('Article Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=100)])
    image_url = StringField('Image URL', validators=[Length(max=300)])

class PaymentMethodForm(FlaskForm):
    method_type = SelectField('Payment Type', 
                            choices=[('paypal', 'PayPal'), ('crypto', 'Cryptocurrency'), ('bank', 'Bank Transfer')],
                            validators=[DataRequired()])
    name = StringField('Payment Method Name', validators=[DataRequired(), Length(min=2, max=100)])
    
    # Crypto fields
    wallet_address = StringField('Wallet Address', validators=[Length(max=200)])
    
    # Bank fields  
    bank_name = StringField('Bank Name', validators=[Length(max=100)])
    account_number = StringField('Account Number', validators=[Length(max=50)])
    routing_number = StringField('Routing Number', validators=[Length(max=20)])
    account_holder = StringField('Account Holder Name', validators=[Length(max=100)])

class CampaignForm(FlaskForm):
    title = StringField('Campaign Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()], widget=TextArea())
    goal_amount = FloatField('Goal Amount ($)', validators=[DataRequired(), NumberRange(min=100)])
    category = SelectField('Category', 
                         choices=[('education', 'Education'), ('medical', 'Medical'), 
                                ('disaster', 'Disaster Relief'), ('community', 'Community'),
                                ('environment', 'Environment'), ('other', 'Other')])
    end_date = DateField('End Date', validators=[DataRequired()])
    image_url = StringField('Image URL')

class NewsForm(FlaskForm):
    title = StringField('News Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()], widget=TextArea())
    image_url = StringField('Image URL')

class PaymentMethodForm(FlaskForm):
    method_type = SelectField('Payment Type', 
                            choices=[('paypal', 'PayPal'), ('crypto', 'Cryptocurrency'), ('bank', 'Bank Transfer')])
    name = StringField('Method Name', validators=[DataRequired(), Length(max=100)])
    wallet_address = StringField('Wallet Address (for crypto)')
    bank_name = StringField('Bank Name (for bank transfer)')
    account_number = StringField('Account Number')
    routing_number = StringField('Routing Number')
    account_holder = StringField('Account Holder Name')
    paypal_email = StringField('PayPal Email (for PayPal)')
