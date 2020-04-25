"""Project settings."""

from os import getenv

DATABASE_HOST = getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_PORT = getenv('DATABASE_PORT', '5432')
DATABASE_NAME = getenv('DATABASE_NAME', 'donkeyengine')
DATABASE_USER = getenv('DATABASE_USER', 'postgres')
DATABASE_PASS = getenv('DATABASE_PASS', '')

SECRET_KEY = getenv('SECRET_KEY', 'lejal_key')
