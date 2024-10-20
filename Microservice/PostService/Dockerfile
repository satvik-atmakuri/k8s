# Use a base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app


# Install any necessary dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y build-essential libpq-dev
RUN pip install psycopg2

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the application will run on
EXPOSE 5000

# Run the application
CMD ["python", "post_service.py"]