from app import db
from app.models import Users, Role
from werkzeug.security import generate_password_hash

# Assuming you have a function or route where you want to create an admin user
def create_admin_user():
    admin = Users(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('Cac2024'),
        role=Role.ADMIN
    )
    db.session.add(admin)
    db.session.commit()
