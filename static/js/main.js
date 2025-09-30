
// Animation and interaction scripts
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Campaign card hover effects
    const campaignCards = document.querySelectorAll('.campaign-card');
    campaignCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.08)';
        });
    });

    // Progress bar animations
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
            bar.style.transition = 'width 1.5s ease-in-out';
        }, 500);
    });

    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Payment method selection
    const paymentMethodSelect = document.getElementById('payment_method');
    if (paymentMethodSelect) {
        paymentMethodSelect.addEventListener('change', function() {
            const selectedMethod = this.value;
            updatePaymentInfo(selectedMethod);
        });
    }

    // Amount quick select buttons
    const amountButtons = document.querySelectorAll('.amount-btn');
    const amountInput = document.getElementById('amount');
    
    amountButtons.forEach(button => {
        button.addEventListener('click', function() {
            const amount = this.dataset.amount;
            if (amountInput) {
                amountInput.value = amount;
            }
            
            // Update active button
            amountButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

function updatePaymentInfo(method) {
    const infoDiv = document.getElementById('payment-info');
    if (!infoDiv) return;
    
    let infoHTML = '';
    
    switch(method) {
        case 'card':
            infoHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-credit-card me-2"></i>
                    Secure payment processing via Stripe. Your card information is encrypted and secure.
                </div>
            `;
            break;
        case 'paypal':
            infoHTML = `
                <div class="alert alert-info">
                    <i class="fab fa-paypal me-2"></i>
                    You'll be redirected to PayPal to complete your donation securely.
                </div>
            `;
            break;
        case 'crypto':
            infoHTML = `
                <div class="alert alert-warning">
                    <i class="fab fa-bitcoin me-2"></i>
                    After clicking donate, you'll receive wallet address and payment instructions.
                </div>
            `;
            break;
        case 'bank':
            infoHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-university me-2"></i>
                    Bank transfer details will be provided after clicking donate. Manual verification may take 1-3 business days.
                </div>
            `;
            break;
    }
    
    infoDiv.innerHTML = infoHTML;
}

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copied to clipboard!', 'success');
    }).catch(function() {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Copied to clipboard!', 'success');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}
