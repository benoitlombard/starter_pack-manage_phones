# Use Python 3.9 as the base image
FROM python:3.12

# Set the working directory within the container
WORKDIR /app

# Copy the requirements.txt file to the container
# COPY requirements.txt /app/pipeline

# Install dependencies using pip
# RUN pip install -r requirements.txt

# Copy the application to the container
COPY . /app

# Expose port 8000
EXPOSE 8000

# Apply migrations to set up the database (SQLite)
RUN python manage_phones_CLI.py

# Run the Django application
CMD python manage_phones_CLI.py runserver 0.0.0.0:8000