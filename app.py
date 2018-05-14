import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.github import make_github_blueprint

app = Flask(__name__)

# Configuration of application, see configuration.py, choose one and uncomment.
app.config.from_object('config.DevelopmentConfig')
# app.config.from_object('configuration.TestingConfig')

github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")
