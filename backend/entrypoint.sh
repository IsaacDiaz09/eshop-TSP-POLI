#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.5
done

echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Seed database
echo "Seeding database..."
python manage.py seed_db
# Start server
echo "Starting Django development server on port 80..."
python manage.py runserver 0.0.0.0:80
