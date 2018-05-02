import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.github import make_github_blueprint
import requests_cache

app = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('config.DevelopmentConfig')
#app.config.from_object('configuration.TestingConfig')

db = SQLAlchemy(app)
requests_cache.install_cache(cache_name='github_cache', backend='sqlite', expire_after=86400)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "RX0NbIGLmdkYRB6")

github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")
