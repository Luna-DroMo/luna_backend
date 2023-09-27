# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the project code into the container
COPY . .

WORKDIR /app/luna

# Run migrations and collect static files
RUN python manage.py makemigrations
RUN python manage.py migrate

# Create Superuser
# ENV DJANGO_SUPERUSER_USERNAME=Dromo
# ENV DJANGO_SUPERUSER_EMAIL=dromo@gmail.com
# ENV DJANGO_SUPERUSER_PASSWORD=Test@1232

# CMD python manage.py createsuperuser --no-input || true && python manage.py runserver 0.0.0.0:8000


# Expose the application port
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]