#!/bin/bash

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is up!"

# Wait for Redis to be ready
echo "Waiting for Redis to be ready..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis is up!"

# Run Django migrations
echo "Running migrations..."
python manage.py migrate

# Start the Django development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000