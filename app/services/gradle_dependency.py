from app.helper.error_handling import MissingParameterException
from app.helper.gpt import get_chat_completion
from flask import jsonify, request
import os

def generate_safe_gradle_dependency(package_name, gradle_version, spring_version):
    try:
        if not package_name:
            raise MissingParameterException('package_name')
        if not gradle_version:
            raise MissingParameterException('gradle_version')
        if not spring_version:
            raise MissingParameterException('spring_version')

        prompt = f'''
        You are an expert in dependency management and secure software development.

        Inputs Provided:
        Package Name: {package_name}
        Gradle Version: {gradle_version}
        Spring Version: {spring_version}

        Task:
        - Provide the Gradle dependency implementation for the given package.
        - The dependency must be the **latest stable version** that is **compatible** with the provided Gradle and Spring versions.
        - Ensure the suggested version has **no known security vulnerabilities** (based on public vulnerability databases like NVD, GitHub advisories, etc.).
        - Output **only** in the format:
          ```
          implementation 'group:artifact:version'
          ```
        - Do not include explanations or extra text.
        - Make sure the dependency is production-ready.
        '''

        response = get_chat_completion(prompt)
        dependency_file_name = f"{package_name}_dependency.txt"
        dependency_file_path = os.path.join("/tmp", dependency_file_name)

        with open(dependency_file_path, "w") as dependency_file:
            dependency_file.write(response.strip())

        return dependency_file_path

    except MissingParameterException as e:
        return jsonify({'error': e.message}), 400

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
