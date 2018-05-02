
class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///application.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	CSRF_ENABLED = True
	SECRET_KEY = ''
	GITHUB_OAUTH_CLIENT_ID = ''
	GITHUB_OAUTH_CLIENT_SECRET = ''

class ProductionConfig(Config):


class DevelopmentConfig(Config):
	DEBUG = True
	OAUTHLIB_INSECURE_TRANSPORT = True

class TestingConfig(Config):
	TESTING = True
