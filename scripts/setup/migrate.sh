#!/bin/bash

# VetrAI Database Migration Script
set -e

echo "🚀 Running VetrAI database migrations..."

# Check if PostgreSQL is running
echo "📊 Checking PostgreSQL connection..."
until PGPASSWORD=vetrai_password psql -h localhost -U vetrai -d vetrai_db -c '\q'; do
  echo "⏳ PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "✅ PostgreSQL is ready!"

# Run initialization script
echo "📝 Running database initialization..."
PGPASSWORD=vetrai_password psql -h localhost -U vetrai -d vetrai_db -f scripts/migration/init.sql

echo "✅ Database migration completed successfully!"
