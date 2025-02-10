FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential

# Upgrade pip and install dependencies
COPY /etls/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ../etls/ /app
COPY ../tables/ /app/tables/

# Run the application
CMD ["python", "main.py"]