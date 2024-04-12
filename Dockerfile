# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install cron and other necessary system utilities
RUN apt-get update && apt-get install -y cron

# Copy the project code into the container
COPY . .

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Change the working directory to /app/luna
WORKDIR /app/luna

RUN touch /var/log/cron.log && chmod 0666 /var/log/cron.log

EXPOSE 8000

# Start the application using the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]