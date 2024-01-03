#!/bin/bash

# Wait for the database to be ready
echo "Waiting for database."


# Apply database migrations
echo "Applying database migrations."
python3 manage.py makemigrations
python3 manage.py migrate

# Start the Django development server
echo "Starting Django server."
python3 manage.py runserver 0.0.0.0:8000

