#!/bin/bash

# Exit on first error
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# The Dockerfile's CMD will run next, starting the Gunicorn server.
# The line below is not strictly needed as Render will execute the CMD,
# but it's good for clarity if you were to run this script manually.
echo "Migrations complete. Starting server..."