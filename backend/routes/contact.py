from flask import Blueprint, request, jsonify
from models import db, ContactInquiry
from .auth import admin_required, token_required

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/', methods=['POST'])
def submit_inquiry():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({'message': 'Missing required fields (name, email, message)'}), 400
        
    new_inquiry = ContactInquiry(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        subject=data.get('subject', 'General Query'),
        message=data.get('message')
    )
    
    db.session.add(new_inquiry)
    db.session.commit()
    
    return jsonify({'message': 'Inquiry submitted successfully. We will get back to you soon!'}), 201

@contact_bp.route('/', methods=['GET'])
@token_required
@admin_required
def get_inquiries(current_user):
    inquiries = ContactInquiry.query.order_by(ContactInquiry.created_at.desc()).all()
    return jsonify([{
        'id': i.id,
        'name': i.name,
        'email': i.email,
        'phone': i.phone,
        'subject': i.subject,
        'message': i.message,
        'status': i.status,
        'created_at': i.created_at.isoformat()
    } for i in inquiries]), 200

@contact_bp.route('/<int:id>/status', methods=['PUT'])
@token_required
@admin_required
def update_inquiry_status(current_user, id):
    data = request.get_json()
    inquiry = ContactInquiry.query.get_or_404(id)
    
    if 'status' in data:
        inquiry.status = data['status']
        db.session.commit()
        
    return jsonify({'message': 'Status updated', 'status': inquiry.status}), 200
