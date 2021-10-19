import os


class Config:
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SECRET_KEY = os.getenv("SECRET_KEY", None)


class DevelopmentConfig(Config):
    pass
