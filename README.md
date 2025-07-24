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
