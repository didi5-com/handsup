# Hands Up - Crowdfunding Platform

## Overview

Hands Up is a Flask-based crowdfunding platform that enables users to create and support charitable campaigns. The platform supports multiple payment methods including credit cards (via Stripe), PayPal, cryptocurrency, and bank transfers. Users can browse campaigns, make donations, and track their contributions while administrators manage campaigns, news articles, and payment methods through a dedicated admin panel.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask**: Core web framework handling routing, request processing, and template rendering
- **Flask-Login**: User session management and authentication
- **Flask-WTF**: Form handling and CSRF protection with WTForms integration
- **Werkzeug**: Password hashing using scrypt algorithm (generates 500-character hashes requiring extended database column lengths)

### Database Layer
- **SQLAlchemy ORM**: Object-relational mapping for database operations
- **PostgreSQL**: Production database (configurable via DATABASE_URL environment variable)
- **SQLite**: Development fallback database
- **Key Models**:
  - `User`: Authentication and profile management with admin role support
  - `Campaign`: Fundraising campaigns with goal tracking and progress calculations
  - `Donation`: Transaction records linking users to campaigns
  - `News`: Content management for platform updates
  - `PaymentMethod`: Manual payment options (crypto wallets, bank accounts)

### Authentication & Security
- Session-based authentication using Flask-Login
- Password hashing with Werkzeug's scrypt implementation (requires 500-char db column)
- CSRF protection on all forms via Flask-WTF
- Admin role-based access control
- Secure configuration via environment variables

### Payment Integration
- **Stripe**: Credit/debit card processing with API key configuration
- **PayPal SDK**: PayPal payment integration (sandbox and live modes)
- **Manual Methods**: Admin-managed cryptocurrency wallets and bank transfer instructions
- Payment flow supports both instant (card/PayPal) and manual verification (crypto/bank)

### Frontend Architecture
- **Jinja2 Templates**: Server-side rendering with template inheritance
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icon library
- **Custom JavaScript**: Form interactions, progress bar animations, payment method toggling
- Template structure uses base.html with content blocks for consistent layouts

### Application Structure
```
/
├── main.py              # Application entry point and routes
├── models.py            # SQLAlchemy database models
├── forms.py             # WTForms form definitions
├── config.py            # Configuration management
├── templates/           # Jinja2 templates
│   ├── base.html
│   ├── admin/          # Admin panel templates
│   ├── auth/           # Login/registration
│   ├── campaigns/      # Campaign listing and details
│   ├── donations/      # Donation flow
│   ├── news/           # News articles
│   └── pages/          # Static pages
└── static/
    ├── css/            # Custom stylesheets
    └── js/             # Client-side scripts
```

### Key Architectural Decisions

**Database Schema Design**
- User model includes is_admin flag for role-based access rather than separate role tables (simpler for small-to-medium scale)
- Campaign progress calculated as property rather than stored field (ensures data consistency)
- Donation model tracks payment_method, status, and reference for flexible payment processing
- PaymentMethod stores configuration as JSON for flexible payment type details

**Template Context Management**
- `moment()` function registered as template global to provide current datetime for calculations
- Avoids template errors when calculating campaign days remaining

**Payment Method Flexibility**
- Hybrid approach: Stripe/PayPal for instant processing, manual methods for crypto/bank transfers
- Manual payment flow creates pending donations then displays instructions rather than direct processing
- Admin can verify and confirm manual payments

**Form Validation Strategy**
- Server-side validation via WTForms with email-validator library dependency
- Client-side validation using Bootstrap classes and custom JavaScript
- Password confirmation via EqualTo validator

**Error Handling Observations**
- Password hash column length must be 500+ characters (scrypt generates longer hashes than default 128)
- Template undefined errors require proper context variable registration
- JSON field access in templates requires proper dict key checking using `.get()` method

## Recent Changes

### September 30, 2025 - Bug Fixes and Deployment Setup
- **Fixed Jinja2 template error**: Updated admin/payments.html to use safe dict access (`.get()`) for payment method details, preventing UndefinedError when optional keys are missing
- **Removed duplicate form classes**: Cleaned up forms.py by removing duplicate CampaignForm, NewsForm, and PaymentMethodForm definitions
- **Fixed JavaScript error**: Updated main.js to handle empty anchor hrefs (`#`) properly, preventing querySelector errors
- **Added deployment files**:
  - `requirements.txt`: Complete list of Python dependencies for easy installation
  - `Dockerfile`: Production-ready containerization setup with gunicorn
  - `.dockerignore`: Excludes unnecessary files from Docker builds
- **Application Status**: Running successfully on port 5000 with all errors resolved