#!/bin/bash
curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
chmod +x wait-for-it.sh

# Wait for the database to be ready
echo "Waiting for database."


# Wait for the database to be ready
./wait-for-it.sh db:5432 -t 60

# Run database migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Start the Django server
python3 manage.py runserver 0.0.0.0:8000

