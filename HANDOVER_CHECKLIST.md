# 🚀 Production Handover Checklist

## ✅ Pre-Deployment Tasks

### 1. Database Initialization
- [ ] Visit: `https://new-pindi-furniture.onrender.com/init-database-secret-2024` (ONCE ONLY)
- [ ] Verify sample data is created
- [ ] Confirm initial users are created (admin/staff)

### 2. Test User Accounts

#### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- [ ] Login successful
- [ ] Can access Dashboard
- [ ] Can access Inventory
- [ ] Can access Orders
- [ ] Can access Production
- [ ] Can access Customers
- [ ] Can access Suppliers
- [ ] Can access Finance ✓ (Admin only)
- [ ] Can access Reports ✓ (Admin only)
- [ ] Can access User Management ✓ (Admin only)
- [ ] Can access Settings ✓ (Admin only)
- [ ] Can export data (Products, Orders, Transactions)

#### Staff Account
- **Username**: `staff`
- **Password**: `staff123`
- [ ] Login successful
- [ ] Can access Dashboard
- [ ] Can access Inventory
- [ ] Can access Orders
- [ ] Can access Production
- [ ] Can access Customers
- [ ] Can access Suppliers
- [ ] **CANNOT** see Finance link in sidebar
- [ ] **CANNOT** see Settings link in sidebar
- [ ] **CANNOT** see Users link in sidebar
- [ ] **CANNOT** access `/finance` directly (403 Forbidden)
- [ ] **CANNOT** access `/reports` directly (403 Forbidden)
- [ ] **CANNOT** access `/settings/users` directly (403 Forbidden)

### 3. Security Checklist

- [ ] **Change Default Passwords**
  - Change `admin` password from `admin123` to a strong password
  - Change `staff` password from `staff123` to a strong password
  - Use: Profile Dropdown → Change Password

- [ ] **Review User Accounts**
  - Delete or disable any test/demo accounts
  - Create real user accounts for client staff
  - Assign appropriate roles (Admin/Staff/Workshop)

- [ ] **Secure the Init Route** (IMPORTANT!)
  - The `/init-database-secret-2024` route should be disabled after first use
  - Consider removing or commenting it out in `app/routes.py` after initialization

### 4. Data Cleanup

- [ ] **Remove Sample Data**
  - Delete sample products
  - Delete sample orders
  - Delete sample customers
  - Delete sample suppliers
  - Delete sample production jobs
  - Delete sample transactions

- [ ] **Add Real Data**
  - Import or manually add real products
  - Add real customer information
  - Add real supplier information
  - Configure actual inventory levels and reorder points

### 5. Configuration Review

- [ ] **Company Settings**
  - Update company name (if needed)
  - Verify currency settings (PKR)
  - Check notification preferences

- [ ] **Email Configuration** (if applicable)
  - Verify email settings for notifications
  - Test email delivery

### 6. Functional Testing

- [ ] **Inventory Management**
  - Add a product
  - Edit a product
  - Delete a product
  - Check low stock alerts

- [ ] **Order Management**
  - Create a new order
  - Edit an order
  - Mark order as delivered
  - Generate invoice PDF

- [ ] **Production Management**
  - Create a production job
  - Update job status
  - Complete a job

- [ ] **Customer Management**
  - Add a customer
  - Edit customer details
  - View customer order history

- [ ] **Supplier Management**
  - Add a supplier
  - Edit supplier details

- [ ] **Finance (Admin Only)**
  - Add a transaction
  - Edit a transaction
  - View financial reports

- [ ] **Reports (Admin Only)**
  - Export products to Excel
  - Export orders to Excel
  - Export transactions to Excel

### 7. Performance & Reliability

- [ ] Test on different devices (Desktop, Tablet, Mobile)
- [ ] Test on different browsers (Chrome, Firefox, Safari, Edge)
- [ ] Verify page load times are acceptable
- [ ] Check that all charts and graphs render correctly
- [ ] Test with slow internet connection

### 8. Documentation for Client

- [ ] **User Guide**
  - How to login
  - How to manage inventory
  - How to create orders
  - How to manage customers/suppliers
  - How to use production tracking
  - How to access reports (Admin)
  - How to manage users (Admin)

- [ ] **Admin Guide**
  - How to create new users
  - How to assign roles
  - How to change passwords
  - How to access financial data
  - How to export reports
  - How to backup data (if applicable)

### 9. Backup & Recovery

- [ ] **Database Backup**
  - Render PostgreSQL has automatic backups
  - Document how to restore from backup
  - Provide client with backup schedule information

- [ ] **Code Repository**
  - Ensure GitHub repository is up to date
  - Provide client with repository access (if needed)
  - Document deployment process

### 10. Final Checks

- [ ] **Environment Variables** (on Render)
  - `DATABASE_URL` - Set correctly
  - `SECRET_KEY` - Strong random value
  - `FLASK_ENV` - Set to `production`

- [ ] **SSL/HTTPS**
  - Verify site loads with HTTPS
  - Check for mixed content warnings

- [ ] **Error Handling**
  - Test 404 page (visit non-existent URL)
  - Verify custom error pages display correctly

- [ ] **Logging**
  - Verify application logs are accessible on Render
  - Check for any error messages in logs

## 📋 Handover Deliverables

### For the Client:

1. **Access Credentials**
   - Admin username and password
   - Render.com dashboard access (if transferring ownership)
   - GitHub repository access (if applicable)

2. **Documentation**
   - User manual (PDF or online)
   - Admin guide
   - Troubleshooting guide
   - Contact information for support

3. **URLs**
   - Production URL: `https://new-pindi-furniture.onrender.com`
   - GitHub Repository: `https://github.com/qureshi08/NPF-1`

4. **Important Notes**
   - Database is persistent (PostgreSQL)
   - Automatic deployments from GitHub main branch
   - Render free tier may sleep after inactivity (first request takes ~30s)
   - Consider upgrading to paid tier for better performance

## 🔒 Post-Handover Security

### Immediate Actions After Handover:

1. **Change All Passwords**
   - Admin account password
   - All user account passwords
   - Render.com account password (if transferred)

2. **Disable Development Routes**
   - Comment out or remove `/init-database-secret-2024` route
   - Remove any debug/test routes

3. **Review Access**
   - Remove your personal access if transferring ownership
   - Ensure only client has admin access

## 📞 Support & Maintenance

- Document any known issues or limitations
- Provide contact information for technical support
- Discuss maintenance and update schedule
- Clarify warranty/support period

---

## ✅ Sign-Off

- [ ] All checklist items completed
- [ ] Client has tested the application
- [ ] Client has received all documentation
- [ ] Client has confirmed acceptance
- [ ] Handover meeting completed

**Date**: _______________
**Signed**: _______________
