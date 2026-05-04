# Use Python 3.9 as the base image
FROM python:3.12

# Set the working directory within the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies using pip
RUN apt-get update && apt-get install -y docker.io # peut etre pertinent de suppr
RUN pip install -r requirements.txt

# Copy the application to the container
COPY . /

# Expose port 8000
EXPOSE 8000

# Apply migrations to set up the database (SQLite)
RUN python manage_phones_CLI.py lists --item-to-show phones 