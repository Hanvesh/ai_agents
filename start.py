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

from app.controllers.experience_controller import experience_bp
from app.controllers.skills_controller import skills_bp
from app.controllers.summary_controller import summary_bp
from app.controllers.prof_alternatives_controller import prof_alt_bp
from app.controllers.testcases_controller import test_case_bp


app = Flask(__name__)

# Register blueprints
app.register_blueprint(experience_bp, url_prefix='/ai-agents')
app.register_blueprint(skills_bp, url_prefix='/ai-agents')
app.register_blueprint(summary_bp, url_prefix='/ai-agents')
app.register_blueprint(prof_alt_bp, url_prefix='/ai-agents')
app.register_blueprint(test_case_bp, url_prefix='/ai-agents')
# app.register_blueprint(docx_bp, url_prefix='/resume-builder-rag')


@app.route('/ai-agents')
def index():
    return 'Hello, World!'
@app.route('/ai-agents/health')
def health_check():
    return 'OK! CPU - {}, Memory - {}'.format(psutil.cpu_percent(2), psutil.virtual_memory().percent), 200


if __name__ == '__main__':
    app.run(debug=True, port=8103)
