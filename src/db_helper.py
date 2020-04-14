"""Module helps with setup test database."""

import os
import subprocess

import psycopg2

from src import settings

TEST_DB_NAME = f'test-{settings.DATABASE_NAME}'


def _execute_query(query):
    """Execute sql in default postgresql database."""
    with psycopg2.connect(database='postgres',
                          user=settings.DATABASE_USER,
                          password=settings.DATABASE_PASS,
                          host=settings.DATABASE_HOST,
                          port=settings.DATABASE_PORT) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query)


def _apply_migrations():
    """Call script to migrate."""
    subprocess.call('src/migrations/migrate.sh',
                    env=dict(os.environ, DATABASE_NAME=TEST_DB_NAME),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


def create_db():
    """Create test database."""
    _execute_query(f'CREATE DATABASE "{TEST_DB_NAME}"')
    _apply_migrations()


def drop_db():
    """Drop test database."""
    _execute_query(f'DROP DATABASE "{TEST_DB_NAME}"')
