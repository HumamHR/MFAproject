<div align="center">

# 🔐 MFAproject

### Defense-in-Depth Authentication for Web Applications

**A Flask-based Multi-Factor Authentication system combining passwords, facial recognition, and OTP verification.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Dlib](https://img.shields.io/badge/Dlib-Face%20Recognition-6A5ACD?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Educational%20Project-orange?style=for-the-badge)

 

</div>


##  Project Overview

**MFAproject** is a security-focused web authentication platform designed to demonstrate the implementation of **Multi-Factor Authentication (MFA)** within a modern web application environment.

The system applies a **defense-in-depth authentication model** by requiring users to pass multiple, independent verification stages rather than relying solely on username and password authentication.

### Core Authentication Layers

* 🔑 **Credential Authentication** — Validates the user's primary identity credentials.
* 👤 **Facial Recognition** — Provides an additional biometric identity-verification layer.
* 🔢 **One-Time Password (OTP)** — Introduces a time-sensitive verification factor.
* 📝 **Security Logging** — Records authentication activity for auditing and monitoring.
* 🌐 **Web-Based Workflow** — Integrates the authentication layers into a unified web application.

By combining these controls into a sequential authentication pipeline, **MFAproject** demonstrates how layered security mechanisms can strengthen identity assurance and reduce the risk of unauthorized access following credential compromise.


<details>
<summary>📸 Screenshots (click to expand)</summary>
<br>

> Add screenshots or a short GIF of the login, face-verification, and OTP screens here, e.g.:
>
> ```markdown
> ![Login screen](docs/screenshots/login.png)
> ![OTP verification](docs/screenshots/otp.png)
> ```

</details>

---

## 🧠 How Authentication Works

```
                    ┌──────────────────────┐
                    │         User         │
                    └───────────┬──────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │     Credentials      │
                    │  Username + Password │
                    └───────────┬──────────┘
                                │
                             Verified
                                │
                                ▼
                    ┌──────────────────────┐
                    │    Biometric Layer   │
                    │   Facial Recognition │
                    └───────────┬──────────┘
                                │
                             Verified
                                │
                                ▼
                    ┌──────────────────────┐
                    │    OTP Verification  │
                    │   One-Time Password  │
                    └───────────┬──────────┘
                                │
                             Verified
                                │
                                ▼
                    ┌──────────────────────┐
                    │     Authenticated    │
                    │        Session       │
                    └──────────────────────┘
```

---

## ✨ Features

| Layer | Feature | Implementation |
|---|---|---|
| 🔑 Credentials | Registration & login | Flask + MySQL, SHA-512 password hashing |
| 🔑 Credentials | Password policy | Enforces length ≥ 10, upper/lowercase, digit, special character |
| 👤 Biometrics | Face enrollment | Captures & stores face samples during registration (`get_faces_from_camera_tkinter.py`) |
| 👤 Biometrics | Face verification | Compares live webcam feed against stored face encodings (`attendance_taker.py`, `features_extraction_to_csv.py`) |
| 🔢 OTP | Email OTP | Generates and emails a one-time code before granting access (`otp_sender.py`) |
| 📝 Auditing | Login logging | Every login attempt (success/failure) is recorded in a `general_logs` MySQL table |
| 🌐 Web UI | Flask templates | Login, registration, OTP, dashboard, tools, resources, legal & about pages |

---

## 🧰 Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | Flask |
| Database | MySQL (via `flask-mysqldb`) |
| Computer vision | Dlib, OpenCV, NumPy, Pillow |
| Data handling | Pandas, SQLite (local attendance/face-log store) |
| Email / OTP | `smtplib`, `pycryptodome` |
| Frontend | HTML, CSS, Jinja2 templates |

---

## 📂 Project Structure

```
MFAproject/
├── log.py                              # Main Flask app: login, register, OTP flow, routing
├── otp_sender.py                       # Generates & emails OTP codes
│
├── Face-racoganintion-based - Copy/
│   ├── attendance_taker.py             # Face_Recognizer class — live webcam face matching
│   └── data/data_dlib/                 # Dlib landmark & ResNet face-recognition models
│
├── data/data_dlib/
│   └── dlib_face_recognition_resnet_model_v1.dat
│
├── loginform - Copy/
│   ├── main.py                         # Earlier/simplified auth prototype (credentials only)
│   └── static/style.css
│
├── templates/
│   ├── index.html                      # Login page
│   ├── register.html                   # Registration page
│   ├── otp.html / otp_login.html       # OTP verification pages
│   ├── home.html / mainpage.html       # Authenticated dashboard
│   ├── Tools.html / resources.html
│   ├── legal.html / About.html
│   └── layout.html                     # Shared page layout
│
└── README.md
```

> **Note:** `get_faces_from_camera_tkinter.py` and `features_extraction_to_csv.py` are imported by `log.py` for face enrollment/feature extraction but aren't shown above if not present in your checkout — make sure they sit alongside `log.py`.

---

## ⚙️ Prerequisites

- **Python 3.12+**
- **MySQL Server** (running locally or reachable over network)
- A **webcam** (for facial enrollment/verification)
- Dlib's pretrained models:
  - `shape_predictor_68_face_landmarks.dat`
  - `dlib_face_recognition_resnet_model_v1.dat`
  (place both under `data/data_dlib/`)
- An **SMTP-capable email account** for sending OTP codes

### Python dependencies

```bash
pip install flask flask-mysqldb mysqlclient dlib opencv-python numpy pandas pillow pycryptodome
```

> Building `dlib` from source requires CMake and a C++ compiler. On Windows, installing a prebuilt wheel or using `conda install -c conda-forge dlib` is usually easier.

---


## 🔍 Security Concepts Demonstrated

- Multi-Factor Authentication (MFA) design
- Password hashing (SHA-512) & complexity enforcement
- Biometric (facial) identity verification
- Time-sensitive OTP verification
- Authentication event logging / auditing
- Defense-in-depth access control

---

## 🛡️ Security Notes

This project is built as a learning/demo implementation of MFA concepts. Before using it beyond a local demo, consider addressing:

- **Secrets management** — database password, Flask secret key, and SMTP credentials are currently hardcoded in `log.py`. Move them to environment variables or a `.env` file (excluded via `.gitignore`), and rotate any credentials that were previously committed.
- **Password hashing** — SHA-512 alone is fast and not ideal for password storage; consider `bcrypt`, `scrypt`, or `argon2` with per-user salts.
- **OTP delivery/storage** — verify OTPs are single-use, time-limited, and never logged in plaintext.
- **Debug mode** — `app.run(debug=True)` should be disabled in any non-local/production environment.
- **SQL logging** — the `general_logs` table currently stores password hashes; consider whether that data is necessary for auditing.

---

## 🧪 Test Scenarios

| Scenario | Expected Result |
|---|---|
| Valid credentials | Proceeds to facial verification |
| Invalid credentials | Login denied, attempt logged |
| Face match | Proceeds to OTP step |
| Face mismatch | Login denied |
| Correct OTP | Session created, access granted |
| Incorrect OTP | Login denied |
| Full chain passed | Authenticated session + log entry |

---

## 🗺️ Roadmap

- [ ] Move all secrets to environment variables
- [ ] Replace SHA-512 with a password-hashing-specific algorithm (bcrypt/argon2)
- [ ] Add rate limiting / lockout after repeated failed attempts
- [ ] Add automated tests for the authentication pipeline
- [ ] Containerize with Docker for easier setup

---

## ❓ FAQ

<details>
<summary><strong>Do I need a webcam to run this?</strong></summary>
<br>
Yes. Facial enrollment (registration) and facial verification (login) both use a live webcam feed via OpenCV/Dlib — there's currently no way to complete either flow without one.
</details>

<details>
<summary><strong>Can I run this without MySQL?</strong></summary>
<br>
Not without changes. Account data and login logs are stored in MySQL via <code>flask-mysqldb</code>. Face-enrollment data is stored separately (SQLite/CSV, depending on the module). Swapping MySQL for SQLite/Postgres would require updating the queries in <code>log.py</code>.
</details>

<details>
<summary><strong>Is this production-ready?</strong></summary>
<br>
No — treat it as an educational reference implementation. See <a href="#️-security-notes">Security Notes</a> for what to fix before using it anywhere beyond a local demo.
</details>

<details>
<summary><strong>What happens if face verification fails but the password was correct?</strong></summary>
<br>
The login is denied and the attempt is written to <code>general_logs</code> — the user never reaches the OTP step without a successful face match.
</details>


---

## 📄 License

This project is available under the MIT License. Add a `LICENSE` file to the repository root to make this explicit.

---

## 🙏 Acknowledgments

- [Dlib](http://dlib.net/) — facial landmark detection & face recognition models
- [Flask](https://flask.palletsprojects.com/) — web framework
- [OpenCV](https://opencv.org/) — computer vision / webcam capture

---

## 👤 Author

**Humam HR**

[![GitHub](https://img.shields.io/badge/GitHub-HumamHR-181717?style=flat-square&logo=github)](https://github.com/HumamHR)

<div align="center">

If this project helped you, consider giving it a ⭐

</div>
