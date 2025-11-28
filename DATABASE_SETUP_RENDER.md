# DATABASE PERSISTENCE SOLUTION FOR RENDER DEPLOYMENT

## ⚠️ CRITICAL ISSUE: Database Wiping on Every Deployment

### Problem
Your application is currently using **SQLite** as the database, which stores data in a file (`furniture.db`). 

**Render uses ephemeral file systems** - this means:
- Every time you deploy, Render creates a fresh container
- Any files created during runtime (including your SQLite database) are **DELETED** on the next deployment
- This is why your data keeps disappearing and sample data reappears

### ✅ SOLUTION: Use PostgreSQL Database

Render provides **persistent PostgreSQL databases** that survive deployments.

## Step-by-Step Setup Instructions

### 1. Create a PostgreSQL Database on Render

1. Go to your Render Dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in the details:
   - **Name**: `npf-database` (or any name you prefer)
   - **Database**: `npf_db`
   - **User**: `npf_user`
   - **Region**: Same as your web service
   - **Plan**: **Free** (for testing) or **Starter** (for production)
4. Click **"Create Database"**
5. Wait for the database to be created (takes ~2 minutes)

### 2. Get the Database Connection String

1. Once created, click on your new database
2. Scroll down to **"Connections"**
3. Copy the **"Internal Database URL"** (starts with `postgres://`)
   - Example: `postgres://npf_user:xxxxx@dpg-xxxxx-a.oregon-postgres.render.com/npf_db`

### 3. Add Database URL to Your Web Service

1. Go to your Render Dashboard
2. Click on your **Web Service** (new-pindi-furniture)
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL you copied
6. Click **"Save Changes"**

### 4. Initialize the Database (ONE TIME ONLY)

After the deployment completes:

1. Visit: `https://new-pindi-furniture.onrender.com/init-database-secret-2024`
2. This will create all tables and add the initial admin user
3. **Important**: This URL has safety protection - it will NOT delete existing data if the database already has users

### 5. Login Credentials

After initialization, you can login with:
- **Username**: `admin`
- **Password**: `admin123`

**⚠️ IMPORTANT**: Change the admin password immediately after first login!

## How It Works

Your application is already configured to support both SQLite and PostgreSQL:

```python
# config.py (already in your code)
database_url = os.environ.get('DATABASE_URL') or 'sqlite:///furniture.db'
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
SQLALCHEMY_DATABASE_URI = database_url
```

- **Local Development**: Uses SQLite (no DATABASE_URL environment variable)
- **Production (Render)**: Uses PostgreSQL (DATABASE_URL is set)

## Verification

After setup, your data will:
- ✅ Persist across deployments
- ✅ Survive server restarts
- ✅ Be backed up by Render (on paid plans)
- ✅ Be production-ready

## Cost

- **Free Tier**: 
  - 90 days of database persistence
  - 1 GB storage
  - Good for testing/demo
  
- **Starter Tier** ($7/month):
  - Unlimited persistence
  - 10 GB storage
  - Daily backups
  - Recommended for production

## Need Help?

If you encounter any issues:
1. Check that DATABASE_URL is set correctly in Environment variables
2. Ensure the database is in the same region as your web service
3. Visit the init URL only once
4. Check Render logs for any connection errors

## Alternative: Backup/Restore Script

If you want to keep using SQLite temporarily, you can:
1. Download the database file before each deployment
2. Re-upload it after deployment

But this is NOT recommended for production use.
