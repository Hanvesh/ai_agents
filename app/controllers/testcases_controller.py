from flask import Blueprint, request, jsonify,send_file
import os
from app.services.testcases import generate_test_cases

test_case_bp = Blueprint('test_case', __name__)

@test_case_bp.route('/generate-test-cases', methods=['POST'])
def create_test_case_controller():
    if 'java_class_file' not in request.files:
        return jsonify({'error': 'java_class_file is required'}), 400
    
    java_class_file = request.files['java_class_file']
    java_class_code = java_class_file.read().decode('utf-8').strip()
    java_class_name = os.path.splitext(java_class_file.filename)[0]
    
    test_case_file_path = generate_test_cases(java_class_code, java_class_name)
    return send_file(test_case_file_path, as_attachment=True, download_name=os.path.basename(test_case_file_path))