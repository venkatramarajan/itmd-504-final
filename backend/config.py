import os
from datetime import timedelta
import secrets
import logging

logger = logging.getLogger(__name__)

class Config:
    # Generate secure random keys if not set in environment
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    
    # Database configuration
    DB_USER = os.environ.get('DB_USER', 'address_book_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'your_secure_password')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'address_book')
    
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'

    def __init__(self):
        logger.debug(f"Database URI: mysql://{self.DB_USER}:****@{self.DB_HOST}/{self.DB_NAME}") 