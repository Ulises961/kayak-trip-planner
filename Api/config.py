import os
from dotenv import load_dotenv
load_dotenv()

class Config:
     SQLALCHEMY_TRACK_MODIFICATIONS = True
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")
    SECRET_KEY="411cd120ade053d5a3e06ef19249444e78360e0b"
class TestingConfig(Config):
    TESTING = True
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    SECRET_KEY="dbb60a26cae08641ea6194a5b540c926d55ab9d7"
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("STAGING_DATABASE_URL")
    SECRET_KEY="28663d35ef0238755fcb2521ec28e8faf0f6f2ae"
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")
    SECRET_KEY="2e4308e056bb7c0e464199a74f68223eb82097e2"
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig
}