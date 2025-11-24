# New Pindi Furniture Admin Portal - Implementation Plan

## 1. Project Overview
**Name:** New Pindi Furniture Admin Portal
**Type:** Manufacturing & Retail Management System
**Tech Stack:**
- **Backend:** Python, Flask
- **Database:** Microsoft SQL Server
- **ORM:** SQLAlchemy (with pyodbc driver)
- **Frontend:** HTML5, Jinja2, Bootstrap 5, JavaScript (Chart.js for analytics)
- **PDF Generation:** WeasyPrint or ReportLab
- **Excel Export:** Pandas / OpenPyXL

## 2. Site Architecture & Modules

### 1. Dashboard
- **Overview:** Key metrics (Total Sales, Pending Orders, Low Stock, Production Status).
- **Visuals:** Sales trend chart, Revenue vs Expense chart.

### 2. Inventory Management
- **Features:** CRUD for Products & Raw Materials.
- **Fields:** SKU, Name, Category, Cost Price, Selling Price, Stock Quantity, Reorder Level, Supplier.
- **Alerts:** Low stock notifications.

### 3. Orders Management (Sales)
- **Features:** Create Order, Update Status (Pending, Processing, Shipped, Delivered, Cancelled).
- **Invoicing:** Generate PDF Invoice.
- **Type:** Retail (Showroom) & Custom (Manufacturing).

### 4. Customer Management (CRM)
- **Features:** Customer profiles, Order History, Contact Info, Loyalty Points.

### 5. Supplier Management
- **Features:** Supplier Database, Purchase Orders, Supply History.

### 6. Finance & Accounting
- **Features:** Record Expenses (Rent, Utilities, Salaries), Track Revenue (from Orders), Profit/Loss Statement.

### 7. Production / Workshop
- **Features:** Job Cards, Material Assignment, Worker Assignment, Status Tracking (Queued, Cutting, Assembling, Polishing, Finished).

### 8. User Management
- **Roles:** Admin (Full Access), Staff (Sales/Inventory), Workshop (Production View).

### 9. Reports & Analytics
- **Reports:** Sales by Period, Top Selling Items, Low Stock Report, Financial Statement.
- **Export:** CSV/Excel.

### 10. Settings
- **Features:** Company Info, Tax Rates, Currency, Backup/Restore (manual).

## 3. Database Schema (SQL Server via SQLAlchemy)

**Users**
- id (PK), username, password_hash, role, email, created_at

**Customers**
- id (PK), name, phone, email, address, loyalty_points, created_at

**Suppliers**
- id (PK), name, contact_person, phone, email, address, created_at

**Categories**
- id (PK), name, type (Material/Product)

**Products** (Inventory)
- id (PK), sku, name, category_id (FK), description, cost_price, selling_price, stock_quantity, reorder_level, supplier_id (FK), image_url

**Orders**
- id (PK), customer_id (FK), order_date, status, total_amount, payment_status, payment_method

**OrderItems**
- id (PK), order_id (FK), product_id (FK), quantity, unit_price, subtotal

**ProductionJobs**
- id (PK), order_id (FK, optional), product_name, description, start_date, due_date, status, assigned_worker

**Transactions** (Finance)
- id (PK), type (Income/Expense), category, amount, date, description, related_order_id (FK, optional)

## 4. Project Directory Structure

```
/new_pindi_furniture
    /app
        __init__.py
        models.py
        routes.py (or split into blueprints)
        forms.py
        utils.py
    /templates
        base.html
        dashboard.html
        /inventory
        /orders
        /customers
        /suppliers
        /finance
        /production
        /users
        /reports
        login.html
    /static
        /css
        /js
        /images
    config.py
    run.py
    requirements.txt
    README.md
```

## 5. Development Steps

1.  **Environment Setup:** Create virtual env, install Flask, SQLAlchemy, PyODBC.
2.  **Database Setup:** Define models, configure SQL Server connection, run migrations/create tables.
3.  **Authentication:** Login/Logout, Role-based decorators.
4.  **Core Modules Implementation:**
    -   Inventory (CRUD)
    -   Customers & Suppliers
    -   Orders & Invoicing
    -   Production
    -   Finance
5.  **Dashboard & Reporting:** Integrate Charts, Export logic.
6.  **Testing:** Manual verification of flows.
