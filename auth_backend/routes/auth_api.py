# auth_backend/routes/auth_api.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from auth_backend.create_app import db
from auth_backend.models import User
from auth_backend.utils.auth_utils import hash_password, check_password, send_verification_email
import random
import string

auth_bp = Blueprint("auth", __name__)


# 🟢 Register Route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # Generate a random verification code
    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    new_user = User(name=name, email=email, password=hash_password(password), is_verified=False, verification_code=verification_code)
    db.session.add(new_user)
    db.session.commit()

    # Send verification email
    send_verification_email(email, verification_code, email_type="register")

    return jsonify({"message": "User registered successfully. Please check your email for the verification code."}), 201


# 🔐 Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password(password, user.password):
        if not user.is_verified:
            return jsonify({"error": "Email not verified. Please verify your email before logging in."}), 403
        access_token = create_access_token(identity=email)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401


# 🔒 Protected Route
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello {current_user}, you are authorized!"}), 200


@auth_bp.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    email = data.get("email")
    code = data.get("code")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.is_verified:
        return jsonify({"message": "User already verified"}), 200
    if user.verification_code == code:
        user.is_verified = True
        user.verification_code = None
        db.session.commit()
        return jsonify({"message": "Email verified successfully"}), 200
    else:
        return jsonify({"error": "Invalid verification code"}), 400

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Generate a reset code
    reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    user.verification_code = reset_code
    db.session.commit()
    send_verification_email(email, reset_code, email_type="forgot")
    return jsonify({"message": "Password reset code sent to your email."}), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    code = data.get("code")
    new_password = data.get("new_password")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.verification_code != code:
        return jsonify({"error": "Invalid reset code"}), 400
    user.password = hash_password(new_password)
    user.verification_code = None
    db.session.commit()
    return jsonify({"message": "Password reset successful. You can now log in with your new password."}), 200

@auth_bp.route("/test-users", methods=["GET"])
def test_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email, "is_verified": u.is_verified} for u in users
    ])
