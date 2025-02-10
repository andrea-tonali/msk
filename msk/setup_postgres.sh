#!/bin/bash

echo "Drop PostgreSQL Container if exists..."
docker stop postgres_msk
docker rmi postgres_msk_image -f
docker rm postgres_msk

# Set Variables
export CONTAINER_NAME="postgres_msk"
export IMAGE_NAME="postgres_msk_image"
export POSTGRES_VERSION="15"
export DB_PORT=5433
export DB_USER="postgres"
export DB_PASSWORD="postgres"
export DB_NAME="msk_db"
export SQL_FILE="msk_db.sql"

# Check if the SQL file exists
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL file '$SQL_FILE' not found!"
    exit 1
fi

echo "Building Docker image for PostgreSQL..."
docker build -t $IMAGE_NAME -<<EOF
FROM postgres:$POSTGRES_VERSION
ENV POSTGRES_USER=$DB_USER
ENV POSTGRES_PASSWORD=$DB_PASSWORD
ENV POSTGRES_DB=$DB_NAME
EOF

echo "Starting PostgreSQL container..."
docker run -d --name $CONTAINER_NAME -p $DB_PORT:5432 -e POSTGRES_USER=$DB_USER -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_DB=$DB_NAME $IMAGE_NAME

echo "Waiting for PostgreSQL to initialize..."
sleep 10

echo "Creating database: $DB_NAME..."
docker exec -i $CONTAINER_NAME psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;" 2>/dev/null

echo "Importing schema from $SQL_FILE..."
cat $SQL_FILE | docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME

echo "Applying Database Migrations..."
alembic upgrade head

echo "Setting up DB URI..."
export POSTGRESQL_DB="postgresql+psycopg2://$DB_USER:$DB_PASSWORD@localhost:$DB_PORT/$DB_NAME"

echo "PostgreSQL setup complete!"