from flask import Flask
import os

import psutil

from dotenv import load_dotenv

env = 'sit'
ENVIRONMENTS = {
    'sit': '.env.sit',
    'qa': '.env.qa',
    'uat': '.env.uat',
    'preprod': '.env.preprod',
    'stage': '.env.stg',
    'production': '.env.prod',
}
path = ENVIRONMENTS[env]

load_dotenv(path)


from app.controllers.testcases_controller import test_case_bp
from app.controllers.gradle_dependencies_controller import gradle_dependency_bp


app = Flask(__name__)

# Register blueprints
app.register_blueprint(test_case_bp, url_prefix='/ai-agents')
app.register_blueprint(gradle_dependency_bp, url_prefix='/ai-agents')
# app.register_blueprint(docx_bp, url_prefix='/resume-builder-rag')


@app.route('/ai-agents')
def index():
    return 'Hello, World!'
@app.route('/ai-agents/health')
def health_check():
    return 'OK! CPU - {}, Memory - {}'.format(psutil.cpu_percent(2), psutil.virtual_memory().percent), 200


if __name__ == '__main__':
    app.run(debug=True, port=8103)
