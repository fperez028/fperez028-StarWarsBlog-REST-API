#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing dependencies..."
pipenv install

echo "Running DB migrations or upgrades..."
pipenv run flask db upgrade

echo "Seeding base data..."
pipenv run python src/seed_data.py

echo "Seeding users..."
pipenv run python src/seed_users.py

echo "Build script completed."
