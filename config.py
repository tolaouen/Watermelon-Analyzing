import os 
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config: 

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SESSION_COOKIE_AGE = os.getenv('SESSION_COOKIE_AGE', timedelta(minutes=10))
    SQLALCHEMY_TRACK_MODIFICATIONS = False