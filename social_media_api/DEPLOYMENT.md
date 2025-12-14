# Social Media API - Deployment Guide

## Prerequisites
- Python 3.11+
- PostgreSQL (for production)
- Git
- Account on deployment platform (Render, Railway, or Heroku)

## Deployment Options

### Option 1: Render.com (Recommended - Free Tier)
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Name: `social-media-api`
   - Environment: `Python`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn social_media_api.wsgi:application`
6. Add environment variables (from .env.example)
7. Click "Create Web Service"

### Option 2: Railway.app
1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Link project: `railway link`
5. Deploy: `railway up`

### Option 3: Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create social-media-api`
4. Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
5. Set config vars: `heroku config:set DEBUG=False SECRET_KEY=your-secret`
6. Deploy: `git push heroku master`

## Environment Variables
Copy `.env.example` to `.env.production` and fill in:
- `SECRET_KEY`: Generate a strong secret key
- `DEBUG`: Set to `False` in production
- Database credentials (PostgreSQL)
- `ALLOWED_HOSTS`: Your domain names
- `CORS_ALLOWED_ORIGINS`: Your frontend domain

## Database Migration
Run migrations on first deploy:
```bash
python manage.py migrate