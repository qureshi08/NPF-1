# New Pindi Furniture - Deployment Guide

## Deploy to Render (Free Hosting)

### Step 1: Prepare Your Code
1. Make sure all files are saved
2. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for deployment"
   ```

### Step 2: Push to GitHub
1. Create a new repository on GitHub: https://github.com/new
2. Name it: `new-pindi-furniture`
3. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/new-pindi-furniture.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: new-pindi-furniture
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Free

5. Add Environment Variables (click "Advanced"):
   - `SECRET_KEY`: `your-secret-key-here-change-this`
   - `PYTHON_VERSION`: `3.11.0`

6. Click "Create Web Service"

### Step 4: Initialize Database
After deployment, you need to initialize the database:
1. Go to your Render dashboard
2. Click on your service
3. Go to "Shell" tab
4. Run:
   ```bash
   python init_db.py
   ```

### Your App Will Be Live At:
`https://new-pindi-furniture.onrender.com`

---

## Alternative: Deploy to PythonAnywhere (Free)

### Step 1: Sign Up
1. Go to https://www.pythonanywhere.com
2. Create a free "Beginner" account

### Step 2: Upload Your Code
1. Go to "Files" tab
2. Upload your project folder or clone from GitHub:
   ```bash
   git clone https://github.com/YOUR_USERNAME/new-pindi-furniture.git
   ```

### Step 3: Create Virtual Environment
In the Bash console:
```bash
cd new-pindi-furniture
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration" → Python 3.10
4. Set:
   - **Source code**: `/home/YOUR_USERNAME/new-pindi-furniture`
   - **Working directory**: `/home/YOUR_USERNAME/new-pindi-furniture`
   - **Virtualenv**: `/home/YOUR_USERNAME/new-pindi-furniture/venv`

5. Edit WSGI configuration file:
   ```python
   import sys
   path = '/home/YOUR_USERNAME/new-pindi-furniture'
   if path not in sys.path:
       sys.path.append(path)

   from run import app as application
   ```

### Step 5: Initialize Database
In Bash console:
```bash
cd new-pindi-furniture
source venv/bin/activate
python init_db.py
```

### Your App Will Be Live At:
`https://YOUR_USERNAME.pythonanywhere.com`

---

## Alternative: Deploy to Railway (Free)

### Step 1: Sign Up
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project"
2. Choose "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Flask and deploy

### Step 3: Initialize Database
1. Click on your service
2. Go to "Settings" → "Variables"
3. Add: `DATABASE_URL` (Railway provides PostgreSQL for free)
4. Open Shell and run:
   ```bash
   python init_db.py
   ```

---

## Login Credentials (After init_db.py)
- **Admin**: username: `admin`, password: `admin123`
- **Staff**: username: `staff`, password: `staff123`

## Important Notes
1. **Free tier limitations**:
   - Render: App sleeps after 15 min of inactivity (takes ~30s to wake up)
   - PythonAnywhere: Always on, but limited to 1 web app
   - Railway: 500 hours/month free

2. **Database**: 
   - SQLite works on PythonAnywhere
   - Render/Railway need PostgreSQL (free tier included)

3. **File uploads**: 
   - May not persist on Render (use cloud storage for production)
   - Work fine on PythonAnywhere

## Recommended: Render
Render is the easiest and most modern option with automatic deployments from GitHub.
