from flask import Blueprint, request, jsonify, send_file
import os
from app.services.crud_auto_generator import generate_crud_from_ddl

crud_generator_bp = Blueprint('crud_generator', __name__)

@crud_generator_bp.route('/generate-crud-from-ddl', methods=['POST'])
def create_crud_from_ddl_controller():
    """
    API Endpoint: /generate-crud-from-ddl
    Request Body:
    {
        "ddl_command": "CREATE TABLE users (id BIGINT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), created_at TIMESTAMP)",
        "package_name": "in.skillzi.user"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body is required'}), 400

    ddl_command = data.get('ddl_command')
    package_name = data.get('package_name')

    if not ddl_command:
        return jsonify({'error': 'ddl_command is required'}), 400
    if not package_name:
        return jsonify({'error': 'package_name is required'}), 400

    output_file_path = generate_crud_from_ddl(ddl_command, package_name)
    return send_file(output_file_path, as_attachment=True, download_name=os.path.basename(output_file_path))
