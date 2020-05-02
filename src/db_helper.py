"""Module helps with setup test database."""

import os
import subprocess

import psycopg2

from src import settings
from src.db import db

TEST_DB_NAME = f'test-{settings.DATABASE_NAME}'


def _execute_query(query, database='postgres'):
    """Execute sql in default postgresql database."""
    with psycopg2.connect(database=database,
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

    # specify test database for gino
    settings.DATABASE_NAME = TEST_DB_NAME

    _apply_migrations()
    return db


def drop_db():
    """Drop test database."""
    _execute_query(f'DROP DATABASE "{TEST_DB_NAME}"')


def truncate_table(table):
    """Truncate table in test database."""
    _execute_query(f'TRUNCATE {table} RESTART IDENTITY CASCADE', TEST_DB_NAME)
