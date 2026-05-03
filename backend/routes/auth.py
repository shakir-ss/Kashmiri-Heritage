from flask import Blueprint, request, jsonify, current_app
from models import db, User, Address
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role not in ['admin', 'sub-admin']:
            return jsonify({'message': 'Admin privileges required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def root_admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Root Admin privileges required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(
        name=data.get('name'),
        email=data.get('email'),
        role=data.get('role', 'customer') # Can be 'admin' during setup
    )
    new_user.set_password(data.get('password'))
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if user and user.check_password(data.get('password')):
        token = jwt.encode({
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")

        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        })

    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/addresses', methods=['GET'])
@token_required
def get_addresses(current_user):
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'phone': a.phone,
        'address_line': a.address_line,
        'city': a.city,
        'state': a.state,
        'country': a.country,
        'pincode': a.pincode,
        'is_default': a.is_default
    } for a in addresses])

@auth_bp.route('/addresses', methods=['POST'])
@token_required
def add_address(current_user):
    data = request.get_json()
    
    # If this is the first address or marked as default, unset others
    is_default = data.get('is_default', False)
    existing = Address.query.filter_by(user_id=current_user.id).count()
    if existing == 0:
        is_default = True
        
    if is_default:
        Address.query.filter_by(user_id=current_user.id).update({'is_default': False})
        
    new_addr = Address(
        user_id=current_user.id,
        name=data.get('name'),
        phone=data.get('phone'),
        address_line=data.get('address_line'),
        city=data.get('city'),
        state=data.get('state'),
        country=data.get('country', 'India'),
        pincode=data.get('pincode'),
        is_default=is_default
    )
    db.session.add(new_addr)
    db.session.commit()
    return jsonify({'message': 'Address added successfully', 'id': new_addr.id}), 201

@auth_bp.route('/addresses/<int:id>', methods=['DELETE'])
@token_required
def delete_address(current_user, id):
    addr = Address.query.get_or_404(id)
    if addr.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(addr)
    db.session.commit()
    return jsonify({'message': 'Address deleted'})
