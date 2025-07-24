from auth_backend.create_app import create_app
from auth_backend.extensions import db

app = create_app()
with app.app_context():
    db.drop_all()      # Purani tables hatao
    db.create_all()    # Nayi tables banao
    print("✅ Database tables created successfully.")