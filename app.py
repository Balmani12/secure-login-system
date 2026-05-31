# =============================================
# SECURE LOGIN SYSTEM - Flask + bcrypt + 2FA
# Run: python app.py
# =============================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pyotp, qrcode, os, re
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db  = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ── DATABASE MODEL ────────────────────────────
class User(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    twofa_secret  = db.Column(db.String(32),  nullable=True)
    twofa_enabled = db.Column(db.Boolean, default=False)

# ── INPUT VALIDATION ──────────────────────────
def is_valid_username(u):
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', u))

def is_valid_email(e):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', e))

def is_strong_password(p):
    return (len(p) >= 8 and
            re.search(r'[A-Z]', p) and
            re.search(r'[a-z]', p) and
            re.search(r'[0-9]', p))

# ── ROUTES ───────────────────────────────────

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# -- REGISTER --
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not is_valid_username(username):
            flash('Username must be 3-20 characters, letters/numbers/underscore only.', 'error')
            return render_template('register.html')

        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('register.html')

        if not is_strong_password(password):
            flash('Password must be 8+ chars with uppercase, lowercase, and number.', 'error')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken. Please choose another.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'error')
            return render_template('register.html')

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user   = User(username=username, email=email, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# -- LOGIN --
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            flash('Invalid username or password.', 'error')
            return render_template('login.html')

        if user.twofa_enabled:
            session['pre_2fa_user_id'] = user.id
            return redirect(url_for('verify_2fa'))

        session['user_id']  = user.id
        session['username'] = user.username
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# -- 2FA VERIFY --
@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'pre_2fa_user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        otp  = request.form.get('otp', '').strip()
        user = User.query.get(session['pre_2fa_user_id'])

        totp = pyotp.TOTP(user.twofa_secret)
        if totp.verify(otp):
            session.pop('pre_2fa_user_id')
            session['user_id']  = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid OTP code. Please try again.', 'error')

    return render_template('verify_2fa.html')

# -- DASHBOARD --
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access the dashboard.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

# -- SETUP 2FA --
@app.route('/setup-2fa', methods=['GET', 'POST'])
def setup_2fa():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        otp    = request.form.get('otp', '').strip()
        secret = session.get('temp_2fa_secret')
        totp   = pyotp.TOTP(secret)

        if totp.verify(otp):
            user.twofa_secret  = secret
            user.twofa_enabled = True
            db.session.commit()
            session.pop('temp_2fa_secret', None)
            flash('2FA enabled successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid OTP. Please scan the QR code again.', 'error')

    secret = pyotp.random_base32()
    session['temp_2fa_secret'] = secret
    totp   = pyotp.TOTP(secret)
    uri    = totp.provisioning_uri(name=user.email, issuer_name='SecureLoginApp')

    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf, format='PNG')
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    return render_template('setup_2fa.html', qr_code=qr_b64, secret=secret)

# -- DISABLE 2FA --
@app.route('/disable-2fa')
def disable_2fa():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    user.twofa_enabled = False
    user.twofa_secret  = None
    db.session.commit()
    flash('2FA has been disabled.', 'success')
    return redirect(url_for('dashboard'))

# -- LOGOUT --
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

# ── RUN ──────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("\n" + "="*45)
        print("  SECURE LOGIN SYSTEM RUNNING")
        print("  Open browser: http://127.0.0.1:5000")
        print("="*45 + "\n")
    app.run(debug=True)