import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super duper secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
