# 🔐 Secure Login System

A production-ready secure web authentication system built with **Flask**, featuring **bcrypt password hashing**, **SQLAlchemy ORM**, **Google Authenticator 2FA (TOTP)**, and comprehensive input validation — implementing OWASP security best practices.

---

## 📌 About

This project was built to demonstrate real-world secure authentication concepts including cryptographic password storage, SQL injection prevention, session security, and multi-factor authentication — key concepts in web application security and OWASP guidelines.

---

## ✨ Features

- ✅ **BCrypt Password Hashing** — Cost factor 12, never stored as plaintext
- ✅ **SQL Injection Prevention** — SQLAlchemy ORM parameterized queries
- ✅ **Google Authenticator 2FA** — TOTP based two-factor authentication
- ✅ **QR Code Generation** — Easy 2FA setup with Google Authenticator app
- ✅ **Input Validation** — Regex based username, email, password validation
- ✅ **Session Management** — Secure HTTPOnly cookies with SameSite policy
- ✅ **Complete Logout** — Full session clearing on logout
- ✅ **Password Strength Enforcement** — Uppercase, lowercase, numbers required
- ✅ **Professional Dark UI** — Clean responsive interface
- ✅ **Flash Messaging** — User friendly error and success messages

---

## 🛡️ Security Implementation

| Security Feature | Implementation |
|---|---|
| Password Storage | BCrypt hashing (cost factor 12) |
| SQL Injection | SQLAlchemy ORM (no raw queries) |
| Session Security | HTTPOnly + SameSite cookies |
| 2FA | TOTP via pyotp (RFC 6238) |
| Input Validation | Regex pattern matching |
| Username Policy | 3-20 chars, alphanumeric only |
| Password Policy | 8+ chars, uppercase + lowercase + number |

---

## 🛠️ Technologies Used

- Python 3
- Flask (Web framework)
- Flask-SQLAlchemy (ORM + SQL injection prevention)
- Flask-Bcrypt (Password hashing)
- PyOTP (TOTP 2FA)
- QRCode (2FA setup QR generation)
- SQLite (Database)
- HTML + CSS (Frontend)

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/Balmani12/secure-login-system

# Navigate to folder
cd secure-login-system

# Install dependencies
pip install flask flask-sqlalchemy flask-bcrypt pyotp qrcode pillow

# Run the application
python app.py

# Open browser
http://127.0.0.1:5000
```

---

## 📱 Pages

```
/register     — Create new account
/login        — Login with credentials
/dashboard    — User dashboard with security status
/setup-2fa    — Enable Google Authenticator 2FA
/verify-2fa   — 2FA verification on login
/disable-2fa  — Disable 2FA
/logout       — Secure logout
```

---

## 📊 Dashboard Security Status

The dashboard displays live security status:
- ✓ BCrypt hashed password confirmation
- ✓ SQL Injection protection status
- ✓ 2FA enabled/disabled status
- ✓ Session security features active

---

## 🔐 OWASP Concepts Covered

- **A02 Cryptographic Failures** — BCrypt hashing prevents plaintext storage
- **A03 Injection** — SQLAlchemy ORM prevents SQL injection
- **A07 Auth Failures** — Strong password policy + 2FA
- **A05 Security Misconfiguration** — Secure session cookies
- **Input Validation** — All user inputs validated before processing

---

## 📚 What I Learned

- Secure password storage with BCrypt cryptographic hashing
- SQL injection prevention using ORM parameterized queries
- Implementing TOTP based two-factor authentication (RFC 6238)
- Flask session management and secure cookie configuration
- OWASP authentication security best practices
- Building production-ready secure web applications

---

## 📂 Project Structure

```
secure-login-system/
├── app.py              # Main Flask application
├── templates/
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── dashboard.html  # User dashboard
│   ├── setup_2fa.html  # 2FA setup page
│   └── verify_2fa.html # 2FA verification page
└── users.db            # SQLite database (auto-created)
```

---

## 👨‍💻 Author

**Balmani**
- 🔗 LinkedIn: [linkedin.com/in/bal-mani-7457a11ba](https://linkedin.com/in/bal-mani-7457a11ba)
- 🐙 GitHub: [github.com/Balmani12](https://github.com/Balmani12)
- 🎯 TryHackMe: [tryhackme.com/p/balmani](https://tryhackme.com/p/balmani)
