#!/bin/bash
set -e

DB_NAME="auth_db"
DB_USER="sakila"

echo "Checking database ${DB_NAME}..."

DB_EXISTS=$(psql -h postgres -U "$DB_USER" -d sakila -tAc \
  "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'")

if [ "$DB_EXISTS" != "1" ]; then
  echo "Creating database ${DB_NAME}..."
  psql -h postgres -U "$DB_USER" -d sakila -c \
    "CREATE DATABASE ${DB_NAME};"
else
  echo "Database ${DB_NAME} already exists"
fi
