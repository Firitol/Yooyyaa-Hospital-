# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hospital-system-secret-key-2025'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///../instance/hospital.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # For production, use: postgres://user:pass@localhost/hospital
