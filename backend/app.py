from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Contact
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

jwt = JWTManager(app)
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    # Create admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

@app.route('/api/register', methods=['POST'])
@jwt_required()
def register():
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'is_admin': user.is_admin
        })
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    user_id = get_jwt_identity()
    contacts = Contact.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': c.id,
        'first_name': c.first_name,
        'last_name': c.last_name,
        'email': c.email,
        'street_address': c.street_address,
        'apartment_unit': c.apartment_unit,
        'city': c.city,
        'zip_code': c.zip_code,
        'phone_number': c.phone_number
    } for c in contacts])

@app.route('/api/contacts', methods=['POST'])
@jwt_required()
def create_contact():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    contact = Contact(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        street_address=data['street_address'],
        apartment_unit=data.get('apartment_unit'),
        city=data['city'],
        zip_code=data['zip_code'],
        phone_number=data['phone_number'],
        user_id=user_id
    )
    
    db.session.add(contact)
    db.session.commit()
    return jsonify({'message': 'Contact created successfully'}), 201

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
@jwt_required()
def update_contact(contact_id):
    user_id = get_jwt_identity()
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    data = request.get_json()
    for key, value in data.items():
        setattr(contact, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Contact updated successfully'})

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    user_id = get_jwt_identity()
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 