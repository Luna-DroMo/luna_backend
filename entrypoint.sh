#!/bin/bash

# Wait for the database to be ready
echo "Waiting for database..."
# Add your database waiting logic here

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
