# 🪑 New Pindi Furniture - ERP System

A modern, feature-rich Enterprise Resource Planning (ERP) system for furniture businesses, built with Flask and premium UI/UX.

## ✨ Features

- **📊 Dashboard** - Real-time KPIs, sales trends, and business insights
- **📦 Inventory Management** - Track products, stock levels, and categories
- **🛒 Order Management** - Process orders, generate invoices (PDF)
- **🏭 Production Tracking** - Monitor production jobs and workflows
- **👥 Customer Management** - Customer database with loyalty points
- **🚚 Supplier Management** - Supplier contacts and purchase tracking
- **💰 Finance & Accounting** - Income/expense tracking, profit analysis
- **📈 Reports** - Comprehensive business reports and analytics
- **👤 User Management** - Role-based access (Admin/Staff)

## 🎨 Premium Design

- Modern, rich animations with smooth transitions
- Responsive design that works on all devices
- Gradient backgrounds and sophisticated color schemes
- Professional typography with Inter font
- Elegant hover effects and micro-interactions

## 🚀 Quick Start (Local)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   python init_db.py
   ```

3. **Run Application**
   ```bash
   python run.py
   ```

4. **Access Application**
   - URL: http://localhost:5000
   - Admin: username: `admin`, password: `admin123`
   - Staff: username: `staff`, password: `staff123`

## 🌐 Deploy Online (Free)

### Option 1: Render (Recommended)
1. Run the preparation script:
   ```bash
   .\deploy-prepare.ps1
   ```

2. Create GitHub repository and push code

3. Deploy on Render:
   - Go to https://render.com
   - Sign up (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Click "Create Web Service"

4. Your app will be live at: `https://your-app-name.onrender.com`

### Option 2: PythonAnywhere
- Always-on free hosting
- Perfect for SQLite database
- See `DEPLOYMENT.md` for full instructions

### Option 3: Railway
- Modern platform with auto-deployments
- Free PostgreSQL database included
- See `DEPLOYMENT.md` for full instructions

## 📖 Full Deployment Guide

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed step-by-step instructions for all platforms.

## 🛠️ Tech Stack

- **Backend**: Flask 3.0, SQLAlchemy
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Database**: SQLite (local) / PostgreSQL (production)
- **Authentication**: Flask-Login
- **PDF Generation**: ReportLab
- **Excel Export**: Pandas, OpenPyXL

## 📁 Project Structure

```
NPF 1/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── routes.py            # Application routes
│   ├── forms.py             # WTForms
│   ├── utils.py             # Utility functions
│   ├── static/
│   │   └── style.css        # Premium animations & styles
│   └── templates/           # HTML templates
├── config.py                # Configuration
├── run.py                   # Application entry point
├── init_db.py               # Database initialization
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment configuration
└── DEPLOYMENT.md            # Deployment guide

```

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Regularly update dependencies

## 📝 License

This project is for educational and commercial use.

## 🤝 Support

For issues or questions, please create an issue in the repository.

---

**Made with ❤️ for New Pindi Furniture**
