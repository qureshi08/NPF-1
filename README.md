# New Pindi Furniture - Inventory Management System

A comprehensive web-based inventory and business management system built with Flask for furniture manufacturing and retail operations.

## 🚀 Live Application

**Production URL**: [https://new-pindi-furniture.onrender.com](https://new-pindi-furniture.onrender.com)

## ✨ Features

### Core Modules
- **📦 Inventory Management** - Track products, stock levels, and reorder points
- **🛒 Order Management** - Create, track, and manage customer orders with PDF invoices
- **🏭 Production Tracking** - Monitor production jobs and workshop activities
- **👥 Customer Management** - Maintain customer database and order history
- **🚚 Supplier Management** - Track suppliers and procurement
- **💰 Finance Module** - Transaction tracking and financial reporting (Admin only)
- **📊 Reports & Analytics** - Export data and view business insights (Admin only)
- **👤 User Management** - Role-based access control (Admin/Staff/Workshop)

### Key Features
- **Role-Based Access Control (RBAC)** - Secure access based on user roles
- **Real-time Notifications** - Low stock alerts and system notifications
- **Data Export** - Export products, orders, and transactions to Excel
- **PDF Invoice Generation** - Professional invoices for customer orders
- **Dashboard Analytics** - Charts and KPIs for business insights
- **Mobile Responsive** - Works seamlessly on desktop, tablet, and mobile
- **Dark Mode Sidebar** - Modern, professional UI design

## 🔐 User Roles

### Admin
- Full system access
- User management
- Finance and reporting
- All CRUD operations

### Staff
- Inventory management
- Order processing
- Customer and supplier management
- Production tracking
- **No access** to finance, reports, or user management

### Workshop
- Production job tracking
- Basic inventory viewing

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Frontend**: Bootstrap 5, Chart.js
- **Deployment**: Render.com
- **Version Control**: Git/GitHub

## 📋 Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (for production)
- Git

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/qureshi08/NPF-1.git
cd NPF-1
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python init_db.py
```

5. **Run the application**
```bash
python run.py
```

6. **Access the application**
- Open browser: `http://localhost:5000`
- Default Admin: `admin` / `admin123`
- Default Staff: `staff` / `staff123`

## 🚀 Production Deployment (Render.com)

### First-Time Setup

1. **Create Render Account** at [render.com](https://render.com)

2. **Create PostgreSQL Database**
   - New → PostgreSQL
   - Name: `npf-database`
   - Copy the **Internal Database URL**

3. **Create Web Service**
   - New → Web Service
   - Connect GitHub repository: `qureshi08/NPF-1`
   - Settings:
     - **Name**: `new-pindi-furniture`
     - **Environment**: `Python 3`
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn run:app`

4. **Environment Variables**
   - `DATABASE_URL`: [Paste Internal Database URL]
   - `SECRET_KEY`: [Generate random string]
   - `FLASK_ENV`: `production`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

6. **Initialize Database** (ONE TIME ONLY)
   - Visit: `https://new-pindi-furniture.onrender.com/init-database-secret-2024`
   - This creates sample data and initial users

### Automatic Deployments

- Push to `main` branch triggers automatic deployment
- Deployment takes ~2-3 minutes

## 👥 Default User Accounts

After database initialization:

| Username | Password | Role | Access Level |
|----------|----------|------|--------------|
| admin | admin123 | Admin | Full Access |
| staff | staff123 | Staff | Limited Access |

**⚠️ IMPORTANT**: Change these passwords immediately after first login!

## 📖 User Guide

### For Administrators

1. **User Management**
   - Navigate to: Users (sidebar)
   - Create new users with appropriate roles
   - Edit or delete existing users
   - Change user passwords

2. **Finance Management**
   - Navigate to: Finance (sidebar)
   - Add income/expense transactions
   - View financial reports
   - Track revenue and profitability

3. **Reports & Analytics**
   - Export products to Excel
   - Export orders to Excel
   - Export transactions to Excel
   - View dashboard analytics

### For All Users

1. **Inventory Management**
   - Add/Edit/Delete products
   - Track stock levels
   - Set reorder points
   - Receive low stock alerts

2. **Order Processing**
   - Create new orders
   - Update order status
   - Generate PDF invoices
   - Track order history

3. **Customer Management**
   - Add customer information
   - View customer order history
   - Update customer details

4. **Production Tracking**
   - Create production jobs
   - Update job status
   - Track completion

## 🔒 Security Features

- Password hashing with Werkzeug
- Role-based access control (RBAC)
- Protected routes with decorators
- Session management with Flask-Login
- CSRF protection
- SQL injection prevention (SQLAlchemy ORM)

## 📁 Project Structure

```
NPF-1/
├── app/
│   ├── templates/          # HTML templates
│   ├── static/            # CSS, JS, images
│   ├── models.py          # Database models
│   ├── routes.py          # Application routes
│   └── __init__.py        # App initialization
├── instance/              # Instance-specific files
├── build.sh              # Render build script
├── config.py             # Configuration
├── init_db.py            # Database initialization
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
├── Procfile             # Render process file
├── runtime.txt          # Python version
├── FEATURES.md          # Detailed feature list
├── HANDOVER_CHECKLIST.md # Client handover guide
└── README.md            # This file
```

## 🐛 Troubleshooting

### Database Issues
- **Problem**: Database not initialized
- **Solution**: Visit `/init-database-secret-2024` route once

### Login Issues
- **Problem**: Cannot login
- **Solution**: Ensure database is initialized with default users

### Deployment Issues
- **Problem**: App not loading on Render
- **Solution**: Check Render logs for errors, verify environment variables

### Performance Issues
- **Problem**: Slow first load
- **Solution**: Render free tier sleeps after inactivity (~30s wake time)

## 📞 Support

For technical support or questions:
- **GitHub Issues**: [https://github.com/qureshi08/NPF-1/issues](https://github.com/qureshi08/NPF-1/issues)
- **Email**: muhammadanasq@gmail.com

## 📄 License

This project is proprietary software developed for New Pindi Furniture.

## 🙏 Acknowledgments

- Built with Flask framework
- UI powered by Bootstrap 5
- Charts by Chart.js
- Icons by Font Awesome
- Deployed on Render.com

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: Production Ready ✅
