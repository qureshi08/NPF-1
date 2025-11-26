# 🧪 NPF-1 Feature Testing Guide

## ✅ Features Successfully Added & Integrated

### 1. 💰 Payment Installments
- **Status:** ✅ Backend & UI Ready
- **How to test:**
  1. Go to any **Order** page.
  2. Click **"Record Payment"**.
  3. Enter amount and method.
  4. Verify order status updates (Unpaid → Partial → Paid).
  5. Click **"View Payment History"** to see the log.

### 2. 📊 Advanced Analytics (Merged into Reports)
- **Status:** ✅ Backend & UI Ready
- **How to test:**
  1. Click **"Reports"** in the sidebar.
  2. **Verify Dashboard:** Check the new summary cards (Revenue, Cost, Profit, Inventory).
  3. **Verify Charts:** Sales Trend and Top Products.
  4. **Verify Tables:** Product Profitability and Top Customers.

### 3. 🔍 Global Search
- **Status:** ✅ Backend & UI Ready
- **How to test:**
  1. Use the **Search Bar** in the top header (top right).
  2. Type "Sofa", "Ali", "#1", or a Supplier name.
  3. Click on a result to navigate to that record.

### 4. 🚨 Low Stock Alerts
- **Status:** ✅ Backend & UI Ready
- **How to test:**
  1. Check the **Notification Bell** in the header.
  2. If stock is low, you will see a warning.
  3. To force a check, visit `/check-low-stock`.

### 5. 📋 Order History
- **Status:** ✅ Backend Logging Active
- **Note:** Actions are logged to the database. Timeline view is coming soon.

---

## 📝 Quick Setup Steps (If needed)

### Step 1: Update Database Schema
```
Visit: https://new-pindi-furniture.onrender.com/update-schema-2024
```
*Only needed if you haven't run it yet.*

### Step 2: Initialize Database (Safe)
```
Visit: https://new-pindi-furniture.onrender.com/init-database-secret-2024
```
*Only needed if database is empty.*
