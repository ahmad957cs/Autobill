# SmartBillCalc Backend

A powerful backend service for automated bill/receipt processing, OCR extraction, and calculation, with secure authentication. Built using Flask, Tesseract OCR, and modern Python libraries.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [API Endpoints](#api-endpoints)
6. [Authentication & Authorization](#authentication--authorization)
7. [Project Structure](#project-structure)
8. [Development & Testing](#development--testing)
9. [Improvements & Changelog](#improvements--changelog)
10. [Best Practices & Recommendations](#best-practices--recommendations)
11. [References & Further Reading](#references--further-reading)

---

## Project Overview
SmartBillCalc Backend is a Flask-based RESTful service that processes bill images, extracts text using OCR, parses mathematical expressions, and provides secure user authentication. It is designed for mobile and web apps needing automated bill/receipt digitization and calculation.

---

## Features
- **Bill Image Upload & Processing**: Upload images (PNG, JPG, JPEG, GIF, BMP) for automated processing.
- **OCR Text Extraction**: Uses Tesseract OCR for high-accuracy text recognition, including handwritten bills.
- **Mathematical Expression Parsing**: Detects and evaluates totals, line items, and calculations from extracted text.
- **Advanced Filtering**: Ignores numbers in product names (e.g., '7UP', '5 Star') and only treats numbers at line ends or after currency symbols as prices.
- **RESTful API**: Clean, well-documented endpoints for integration.
- **Authentication & Authorization**: JWT-based user registration, login, email verification, password reset, and protected routes.
- **CORS Support**: Cross-origin resource sharing for frontend integration.
- **Robust Error Handling**: Handles invalid images, OCR failures, and malformed requests gracefully.
- **Test Suite**: Automated tests for API and OCR logic.
- **Production Ready**: Gunicorn support, environment-based config, and SQLite database for users.

---

## Technologies Used
- **Python 3.8+**
- **Flask** (web framework)
- **Flask-CORS** (CORS support)
- **Flask-JWT-Extended** (JWT authentication)
- **Tesseract OCR** via **pytesseract**
- **OpenCV** (image preprocessing)
- **Pillow** (image handling)
- **NumPy** (array processing)
- **Werkzeug** (WSGI utilities)
- **Gunicorn** (production WSGI server)
- **Requests** (HTTP requests)
- **python-dotenv** (environment management)
- **SQLite** (user database)

---

## Setup Instructions

### Prerequisites
1. **Python 3.8+**
2. **Tesseract OCR**
   - Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

### Installation
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```
2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```
3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
6. **Run the application**
   ```bash
   python app.py
   ```

---

## API Endpoints

### Bill Processing
- `POST /process_bill_image` — Upload and process a bill image, returns extracted text and calculated totals.

### Authentication
- `POST /register` — Register a new user (name, email, password)
- `POST /login` — Login and receive JWT token
- `POST /verify` — Verify email with code
- `POST /forgot-password` — Request password reset code
- `POST /reset-password` — Reset password with code
- `GET /protected` — Example protected route (JWT required)

### Other
- Health check and test endpoints (see test_api.py and Postman collection)

---

## Authentication & Authorization
- **JWT-based authentication** for secure API access
- **Email verification** required for new users
- **Password reset** via email code
- **Protected routes** using JWT tokens

---

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── utils/
│       ├── ocr_engine.py
│       ├── image_processor.py
│       ├── image_processor_simple.py
│       └── math_parser.py
├── auth_backend/
│   ├── models.py
│   ├── config.py
│   ├── extensions.py
│   ├── create_app.py
│   ├── routes/
│   │   └── auth_api.py
│   └── utils/
│       └── auth_utils.py
├── tests/
├── app.py
├── requirements.txt
└── ...
```

---

## Development & Testing
- **Run tests:** `python -m pytest` or `python test_api.py`
- **Format code:** `black .`
- **Lint code:** `flake8`
- **Test setup:** `python test_setup.py`
- **API testing:** Use the provided Postman collection

---

## Improvements & Changelog
### Major 2024 Improvements
- Numbers in product names (e.g., '7UP', '5 Star') are ignored for price extraction
- Only numbers at line ends or after currency symbols are treated as prices
- Known product names with numbers are filtered before calculation
- Calculation logic is more robust and less error-prone
- Handwriting and multi-line bill support improved

### Commercial OCR API Suggestions
- [Google Cloud Vision API](https://cloud.google.com/vision)
- [Microsoft Azure Form Recognizer](https://azure.microsoft.com/en-us/services/form-recognizer/)
- [Amazon Textract](https://aws.amazon.com/textract/)

---

## Best Practices & Recommendations
- Use high-quality, well-lit images for best OCR results
- Capture the entire bill in the frame
- Compress images to under 2MB for faster processing
- Always check the `success` field in API responses
- Implement retry logic and user-friendly error messages in clients
- For production: use HTTPS, rate limiting, authentication, and Gunicorn

---

## References & Further Reading
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [OpenCV](https://opencv.org/)
- [Pillow](https://python-pillow.org/)
- [NumPy](https://numpy.org/)
- [Gunicorn](https://gunicorn.org/)

---

*For any questions or contributions, please open an issue or pull request.* 