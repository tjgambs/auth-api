import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# -- Postgres
SQLALCHEMY_DATABASE_URI = 'postgres://tim:password@localhost:5432/dev'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_TIMEOUT	= 10

# -- Flask
SECRET_KEY = '0656e2821f328bbd4576674e36be05bf35de91bf74ebdf9d'
CACHE_TIMEOUT = 60 * 60 * 15  # 15 minutes

# -- User Auth
TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # 1 Week