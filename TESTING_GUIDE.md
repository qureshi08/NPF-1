# 🧪 NPF-1 Feature Testing Guide

## ✅ Features Successfully Added (Backend Ready)

### 1. 💰 Payment Installments
- **Status:** ✅ Backend complete, ❌ UI pending
- **How to test (via URL):**
  ```
  POST /orders/1/add-payment
  Form data: amount=5000&payment_method=Cash&notes=First installment
  ```
- **What it does:**
  - Records partial payments for orders
  - Auto-updates order payment status (Unpaid → Partial → Paid)
  - Creates transaction records
  - Sends notifications

### 2. 📊 Advanced Analytics Dashboard
- **Status:** ✅ Backend complete, ✅ UI complete
- **How to test:**
  1. Visit: `https://new-pindi-furniture.onrender.com/analytics`
  2. You'll see:
     - Total Revenue, Cost, Profit, Profit Margin
     - Inventory Valuation
     - Product Profitability Analysis (with color-coded margins)
     - Top 10 Customers by Revenue
- **Note:** Need to add link to sidebar manually

### 3. 🔍 Global Search API
- **Status:** ✅ Backend complete, ❌ UI pending
- **How to test:**
  ```
  GET /search?q=sofa
  ```
- **Returns:** JSON with products, customers, orders, suppliers matching "sofa"
- **Example response:**
  ```json
  {
    "results": [
      {
        "type": "Product",
        "icon": "fa-box",
        "title": "3-Seater Sofa",
        "subtitle": "SKU: SOF-001 | Stock: 5",
        "url": "/inventory/edit/1"
      }
    ]
  }
  ```

### 4. 🚨 Low Stock Alerts
- **Status:** ✅ Backend complete
- **How to test:**
  1. Visit: `https://new-pindi-furniture.onrender.com/check-low-stock`
  2. Returns: `{"checked": 5, "alerts_sent": 2}`
  3. Check notifications bell - you'll see low stock alerts

### 5. 📋 Order History Tracking
- **Status:** ✅ Backend complete, ❌ UI pending
- **What it does:**
  - Logs every action on an order (status changes, payments)
  - Stores username, timestamp, details
  - Ready for timeline view

---

## 🚧 What's Missing (Frontend UI)

### To make features fully usable, need to add:

1. **Analytics Link in Sidebar**
   - Add between "Reports" and "Settings"
   - Icon: `fa-chart-pie`

2. **Payment Form on Order View**
   - Add form to `/orders/<id>` page
   - Fields: Amount, Payment Method, Notes
   - Submit to `/orders/<id>/add-payment`

3. **Global Search Bar**
   - Add search input in top navigation
   - Use AJAX to call `/search?q=<query>`
   - Display results in dropdown

4. **Order Timeline View**
   - Create template to show order history
   - Display as vertical timeline with icons

---

## 📝 Quick Testing Steps (After Deployment)

### Step 1: Update Database Schema
```
Visit: https://new-pindi-furniture.onrender.com/update-schema-2024
```
This creates the new tables: `payments`, `order_history`

### Step 2: Test Analytics (Works Now!)
```
Visit: https://new-pindi-furniture.onrender.com/analytics
```
You should see profit analysis, top customers, etc.

### Step 3: Test Global Search API
```
Visit: https://new-pindi-furniture.onrender.com/search?q=sofa
```
You should see JSON response with search results

### Step 4: Test Low Stock Alerts
```
Visit: https://new-pindi-furniture.onrender.com/check-low-stock
```
Then check your notifications bell for alerts

### Step 5: Test Payment (Manual - via browser dev tools)
1. Go to any order page
2. Open browser console
3. Run:
```javascript
fetch('/orders/1/add-payment', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: 'amount=5000&payment_method=Cash&notes=Test'
}).then(r => r.text()).then(console.log)
```

---

## 🎯 Summary

**What Works Right Now:**
- ✅ Analytics Dashboard (just visit `/analytics`)
- ✅ Global Search API (returns JSON)
- ✅ Low Stock Checker (visit `/check-low-stock`)
- ✅ Payment backend (can POST to `/orders/1/add-payment`)

**What Needs UI:**
- ❌ Analytics link in sidebar (manual URL works)
- ❌ Payment form on order page (API works)
- ❌ Search bar in navigation (API works)
- ❌ Order timeline view (data is being logged)

**Next Step:**
I can add all the missing UI components in the next update!
