#!/bin/bash

echo "Starting BodyTune AI Application..."
echo

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True

# Initialize database if it doesn't exist
if [ ! -f bodytune.db ]; then
    echo "Initializing database..."
    python init_db.py
fi

# Start the Flask application
echo "Starting Flask server..."
python app.py
