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


def analyze_gradle_vulnerabilities(build_gradle_content):
    try:
        if not build_gradle_content:
            raise MissingParameterException('build_gradle_content')

        # Extract Spring Boot version
        spring_version_match = re.search(
            r"id\s+'org\.springframework\.boot'\s+version\s+'([\d\.]+)'",
            build_gradle_content
        )
        spring_version = spring_version_match.group(1) if spring_version_match else "Not found"

        # Extract Gradle version (from gradle-wrapper.properties content if present in build.gradle or comments)
        gradle_version_match = re.search(
            r"gradle-(\d+\.\d+(?:\.\d+)*)-",
            build_gradle_content
        )
        gradle_version = gradle_version_match.group(1) if gradle_version_match else "Not found"

        prompt = f'''
        You are an expert in dependency security analysis and Gradle/Spring compatibility.

        Inputs Provided:
        Gradle File Content:
        ```
        {build_gradle_content}
        ```

        Gradle Version: {gradle_version}
        Spring Version: {spring_version}

        Task:
        1. Identify all dependencies in the provided build.gradle file that have **known security vulnerabilities**.
        2. For each vulnerable dependency, suggest the **latest stable version** that:
           - Is compatible with the given Gradle and Spring versions.
           - Has no known vulnerabilities (cross-check against NVD, GitHub Advisories, Maven security reports).
        3. Output the results strictly in this format:
        ```
        Vulnerable Dependency: group:artifact:current_version
        Latest Safe Version: implementation 'group:artifact:safe_version'
        ```
        4. List **only** dependencies that are vulnerable. Do not include non-vulnerable ones.
        5. No extra commentary or explanations — only the above format for each dependency.
        '''

        response = get_chat_completion(prompt)
        output_file_name = "gradle_vulnerability_report.txt"
        output_file_path = os.path.join("/tmp", output_file_name)

        with open(output_file_path, "w") as output_file:
            output_file.write(response.strip())

        return output_file_path

    except MissingParameterException as e:
        return jsonify({'error': e.message}), 400

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
