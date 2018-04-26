import requests_cache

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('config.DevelopmentConfig')
#app.config.from_object('configuration.TestingConfig')

db = SQLAlchemy(app)
requests_cache.install_cache(cache_name='github_cache', backend='sqlite', expire_after=600)
