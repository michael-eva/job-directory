class Config(object):
        DEBUG = False
        TESTING = False
        SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

        DB_NAME = "production-db"
        DB_USERNAME = "admin"
        DB_PASSWORD = "BananasArePeopleToo"
        SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
        pass

class DevelopmentConfig(Config):
        DEBUG = True

        DB_NAME = "development-db"
        DB_USERNAME = "admin"
        DB_PASSWORD = "BananasArePeopleToo"
        SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
        SQLALCHEMY_TRACK_MODIFICATIONS = 'False'


        SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
        TESTING = True

        DB_NAME = "development-db"
        DB_USERNAME = "admin"
        DB_PASSWORD = "BananasArePeopleToo"

        SESSION_COOKIE_SECURE = False
