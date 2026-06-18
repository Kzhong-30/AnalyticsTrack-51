#!/bin/bash

set -e

cd ""/bin"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating upload directory..."
mkdir -p uploads

echo "Seeding database..."
python3 -m app.seed

echo "Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
