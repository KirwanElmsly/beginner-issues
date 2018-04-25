from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')
#app.config.from_object('configuration.TestingConfig')

db = SQLAlchemy(app)

# Here I would set up the cache, a task queue, etc.
