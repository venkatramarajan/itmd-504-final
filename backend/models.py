from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    contacts = db.relationship('Contact', backref='user', lazy=True)

    def set_password(self, password):
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        # Store the hash as a string
        self.password_hash = hashed.decode('utf-8')

    def check_password(self, password):
        try:
            # Convert the stored hash back to bytes
            stored_hash = self.password_hash.encode('utf-8')
            # Hash the provided password with the same salt
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except Exception as e:
            print(f"Error checking password: {str(e)}")
            return False

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    street_address = db.Column(db.String(200), nullable=False)
    apartment_unit = db.Column(db.String(20))
    city = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 