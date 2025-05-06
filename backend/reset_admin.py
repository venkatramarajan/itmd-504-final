from app import app, db
from models import User

with app.app_context():
    # Drop existing admin user if exists
    admin = User.query.filter_by(username='admin').first()
    if admin:
        db.session.delete(admin)
        db.session.commit()
        print("Existing admin user deleted")

    # Create new admin user
    admin = User(username='admin', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("New admin user created successfully!") 