"""
Database Initialization Script
Run this script to create all tables and seed initial data
"""
from app import create_app, db
from app.models import User, Customer, Supplier, Category, Product, Order, OrderItem, ProductionJob, Transaction
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Drop all tables and recreate
    print("Dropping existing tables...")
    db.drop_all()
    
    print("Creating tables...")
    db.create_all()
    
    # Create Admin User
    print("Creating admin user...")
    admin = User(username='admin', email='admin@newpindi.com', role='Admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create Staff User
    staff = User(username='staff', email='staff@newpindi.com', role='Staff')
    staff.set_password('staff123')
    db.session.add(staff)
    
    # Create Categories
    print("Creating categories...")
    cat1 = Category(name='Sofas', type='Product')
    cat2 = Category(name='Beds', type='Product')
    cat3 = Category(name='Tables', type='Product')
    cat4 = Category(name='Wood', type='Material')
    cat5 = Category(name='Fabric', type='Material')
    db.session.add_all([cat1, cat2, cat3, cat4, cat5])
    db.session.commit()
    
    # Create Suppliers
    print("Creating suppliers...")
    sup1 = Supplier(name='Wood Suppliers Ltd', contact_person='Ahmed Khan', 
                    phone='0300-1234567', email='ahmed@woodsuppliers.com',
                    address='Industrial Area, Rawalpindi')
    sup2 = Supplier(name='Fabric House', contact_person='Sara Ali', 
                    phone='0321-9876543', email='sara@fabrichouse.com',
                    address='Saddar, Rawalpindi')
    db.session.add_all([sup1, sup2])
    db.session.commit()
    
    # Create Customers
    print("Creating customers...")
    cust1 = Customer(name='Ali Hassan', phone='0333-1111111', 
                     email='ali@example.com', address='Satellite Town, Rawalpindi',
                     loyalty_points=50)
    cust2 = Customer(name='Fatima Ahmed', phone='0345-2222222',
                     email='fatima@example.com', address='Bahria Town, Rawalpindi',
                     loyalty_points=100)
    cust3 = Customer(name='Usman Malik', phone='0300-3333333',
                     email='usman@example.com', address='DHA, Islamabad',
                     loyalty_points=25)
    db.session.add_all([cust1, cust2, cust3])
    db.session.commit()
    
    # Create Products
    print("Creating products...")
    prod1 = Product(sku='SOF-001', name='3-Seater Sofa', category_id=cat1.id,
                    description='Comfortable 3-seater sofa with premium fabric',
                    cost_price=25000, selling_price=45000, stock_quantity=5,
                    reorder_level=2, supplier_id=sup2.id)
    
    prod2 = Product(sku='BED-001', name='King Size Bed', category_id=cat2.id,
                    description='Solid wood king size bed with headboard',
                    cost_price=35000, selling_price=65000, stock_quantity=3,
                    reorder_level=1, supplier_id=sup1.id)
    
    prod3 = Product(sku='TAB-001', name='Dining Table 6-Seater', category_id=cat3.id,
                    description='Wooden dining table with 6 chairs',
                    cost_price=30000, selling_price=55000, stock_quantity=2,
                    reorder_level=1, supplier_id=sup1.id)
    
    prod4 = Product(sku='SOF-002', name='L-Shape Sofa', category_id=cat1.id,
                    description='Modern L-shape sofa set',
                    cost_price=40000, selling_price=75000, stock_quantity=1,
                    reorder_level=1, supplier_id=sup2.id)
    
    prod5 = Product(sku='BED-002', name='Single Bed', category_id=cat2.id,
                    description='Single bed with storage',
                    cost_price=15000, selling_price=28000, stock_quantity=8,
                    reorder_level=3, supplier_id=sup1.id)
    
    db.session.add_all([prod1, prod2, prod3, prod4, prod5])
    db.session.commit()
    
    # Create Sample Orders
    print("Creating sample orders...")
    order1 = Order(customer_id=cust1.id, 
                   order_date=datetime.utcnow() - timedelta(days=5),
                   status='Delivered', payment_status='Paid',
                   payment_method='Cash', total_amount=45000)
    
    item1 = OrderItem(order_id=order1.id, product_id=prod1.id,
                     quantity=1, unit_price=45000, subtotal=45000)
    order1.items.append(item1)
    
    order2 = Order(customer_id=cust2.id,
                   order_date=datetime.utcnow() - timedelta(days=2),
                   status='Processing', payment_status='Partial',
                   payment_method='Bank Transfer', total_amount=120000)
    
    item2 = OrderItem(order_id=order2.id, product_id=prod2.id,
                     quantity=1, unit_price=65000, subtotal=65000)
    item3 = OrderItem(order_id=order2.id, product_id=prod3.id,
                     quantity=1, unit_price=55000, subtotal=55000)
    order2.items.extend([item2, item3])
    
    order3 = Order(customer_id=cust3.id,
                   order_date=datetime.utcnow(),
                   status='Pending', payment_status='Unpaid',
                   payment_method='', total_amount=28000)
    
    item4 = OrderItem(order_id=order3.id, product_id=prod5.id,
                     quantity=1, unit_price=28000, subtotal=28000)
    order3.items.append(item4)
    
    db.session.add_all([order1, order2, order3])
    db.session.commit()
    
    # Create Production Jobs
    print("Creating production jobs...")
    job1 = ProductionJob(order_id=order2.id, product_name='King Size Bed',
                        description='Custom king size bed for Order #2',
                        due_date=datetime.utcnow() + timedelta(days=7),
                        status='Assembling', assigned_worker='Rashid')
    
    job2 = ProductionJob(product_name='Custom Wardrobe',
                        description='6-door wardrobe with mirror',
                        due_date=datetime.utcnow() + timedelta(days=10),
                        status='Cutting', assigned_worker='Imran')
    
    job3 = ProductionJob(product_name='Office Desk',
                        description='Executive office desk',
                        due_date=datetime.utcnow() + timedelta(days=5),
                        status='Polishing', assigned_worker='Kamran')
    
    db.session.add_all([job1, job2, job3])
    db.session.commit()
    
    # Create Transactions
    print("Creating financial transactions...")
    # Income from orders
    txn1 = Transaction(type='Income', category='Sales',
                      amount=45000, description='Order #1 - 3-Seater Sofa',
                      related_order_id=order1.id,
                      date=datetime.utcnow() - timedelta(days=5))
    
    # Expenses
    txn2 = Transaction(type='Expense', category='Rent',
                      amount=50000, description='Monthly shop rent',
                      date=datetime.utcnow() - timedelta(days=10))
    
    txn3 = Transaction(type='Expense', category='Utilities',
                      amount=8000, description='Electricity bill',
                      date=datetime.utcnow() - timedelta(days=8))
    
    txn4 = Transaction(type='Expense', category='Salaries',
                      amount=150000, description='Monthly staff salaries',
                      date=datetime.utcnow() - timedelta(days=3))
    
    txn5 = Transaction(type='Income', category='Sales',
                      amount=60000, description='Partial payment Order #2',
                      related_order_id=order2.id,
                      date=datetime.utcnow() - timedelta(days=2))
    
    db.session.add_all([txn1, txn2, txn3, txn4, txn5])
    db.session.commit()
    
    print("\n" + "="*50)
    print("Database initialized successfully!")
    print("="*50)
    print("\nLogin Credentials:")
    print("-" * 50)
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nStaff:")
    print("  Username: staff")
    print("  Password: staff123")
    print("-" * 50)
    print("\nSample Data Created:")
    print(f"  - {User.query.count()} Users")
    print(f"  - {Category.query.count()} Categories")
    print(f"  - {Supplier.query.count()} Suppliers")
    print(f"  - {Customer.query.count()} Customers")
    print(f"  - {Product.query.count()} Products")
    print(f"  - {Order.query.count()} Orders")
    print(f"  - {ProductionJob.query.count()} Production Jobs")
    print(f"  - {Transaction.query.count()} Transactions")
    print("="*50)
