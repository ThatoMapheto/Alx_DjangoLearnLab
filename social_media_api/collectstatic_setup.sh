#!/bin/bash
echo "Setting up static files for production..."

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Run collectstatic
python manage.py collectstatic --noinput

echo "Static files collected to staticfiles/"
echo "For production with S3, configure AWS credentials and run:"
echo "python manage.py collectstatic --noinput"
