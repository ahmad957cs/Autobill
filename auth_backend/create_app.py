# auth_backend/create_app.py

from flask import Flask
from auth_backend.extensions import db, bcrypt, jwt
from auth_backend.routes.auth_api import auth_bp
from auth_backend.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
