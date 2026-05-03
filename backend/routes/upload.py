import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"message": "No image part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"message": "No selected image"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        unique_name = str(uuid.uuid4()) + ext
        
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_name)
        
        try:
            cloudinary_url = os.environ.get('CLOUDINARY_URL')
            if cloudinary_url:
                import cloudinary.uploader
                result = cloudinary.uploader.upload(file)
                return jsonify({"image_url": result.get('secure_url')}), 200
        except Exception as e:
            pass # fallback to local

        file.save(file_path)
        # Return URL relative path
        return jsonify({"image_url": f"/static/uploads/{unique_name}"}), 200
