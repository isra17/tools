import os


class Config:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ["SECRET_KEY"]


class DevelopmentConfig(Config):
    pass
