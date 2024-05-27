#!/bin/bash
curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
chmod +x wait-for-it.sh

# Wait for the database to be ready
echo "Waiting for database."

# Wait for the database to be ready
./wait-for-it.sh db:5432 -t 60

# Enable cron
cron

# python3 manage.py makemigrations # This part can cause some conflicts some commented out.
python3 manage.py makemigrations
python3 manage.py migrate

# Start the cron server
# python3 manage.py runcrons &

# Start the Django server
python3 manage.py runserver 0.0.0.0:8000 &

echo "Starting django-cron jobs..."
# while true; do
#     python3 manage.py runcrons
#     sleep 3600
# done

