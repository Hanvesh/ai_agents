from flask import Blueprint, request, jsonify, send_file
import os
from app.services.gradle_dependency import generate_safe_gradle_dependency

gradle_dependency_bp = Blueprint('gradle_dependency', __name__)

@gradle_dependency_bp.route('/generate-safe-gradle-dependency', methods=['POST'])
def create_gradle_dependency_controller():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body is required'}), 400

    package_name = data.get('package_name')
    gradle_version = data.get('gradle_version')
    spring_version = data.get('spring_version')

    if not package_name:
        return jsonify({'error': 'package_name is required'}), 400
    if not gradle_version:
        return jsonify({'error': 'gradle_version is required'}), 400
    if not spring_version:
        return jsonify({'error': 'spring_version is required'}), 400

    dependency_file_path = generate_safe_gradle_dependency(package_name, gradle_version, spring_version)
    return send_file(dependency_file_path, as_attachment=True, download_name=os.path.basename(dependency_file_path))


@gradle_vulnerability_bp.route('/analyze-gradle-vulnerabilities', methods=['POST'])
def analyze_gradle_vulnerabilities_controller():
    # Expecting a file upload containing build.gradle content
    if 'file' not in request.files:
        return jsonify({'error': 'build.gradle file is required'}), 400

    gradle_file = request.files['file']
    if gradle_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read the file content
    build_gradle_content = gradle_file.read().decode('utf-8')

    # Run the vulnerability analysis
    output_file_path = analyze_gradle_vulnerabilities(build_gradle_content)

    return send_file(output_file_path, as_attachment=True, download_name=os.path.basename(output_file_path))
