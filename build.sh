#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Database initialization removed - use /init-database-secret-2024 endpoint for first-time setup
# DO NOT run init_db.py here as it will wipe all production data on every deployment!
