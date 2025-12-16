#!/bin/bash

# Create data directory if it doesn't exist
mkdir -p /app/data

echo "Running database migrations..."
alembic upgrade head

echo "Database initialization complete!"