from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, send_file, make_response, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Product, Order, Customer, Supplier, Transaction, ProductionJob, OrderItem, Category
from app.forms import LoginForm, ProductForm, OrderForm, CustomerForm, SupplierForm, TransactionForm, ProductionJobForm
from app.utils import role_required, generate_pdf_invoice, export_to_excel, export_to_csv, get_low_stock_items
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from werkzeug.utils import secure_filename
import os
import io

main_bp = Blueprint('main', __name__)

# ==================== AUTHENTICATION ====================

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app.utils import log_action
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # Log failed login attempt
            log_action(
                action=f'Failed login attempt for username: {form.username.data}',
                entity_type='User',
                details='Invalid credentials'
            )
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        # Log successful login
        log_action(
            action=f'User logged in: {user.username}',
            entity_type='User',
            entity_id=user.id,
            details=f'Successful login'
        )
        flash(f'Welcome back, {user.username}!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@main_bp.route('/logout')
def logout():
    from app.utils import log_action
    if current_user.is_authenticated:
        log_action(
            action=f'User logged out: {current_user.username}',
            entity_type='User',
            entity_id=current_user.id
        )
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# ==================== DASHBOARD ====================

@main_bp.route('/')
@login_required
def index():
    # Dashboard Stats
    total_sales = db.session.query(func.sum(Order.total_amount)).filter(Order.payment_status == 'Paid').scalar() or 0
    pending_orders = Order.query.filter_by(status='Pending').count()
    low_stock_count = Product.query.filter(Product.stock_quantity <= Product.reorder_level).count()
    active_jobs = ProductionJob.query.filter(ProductionJob.status != 'Finished').count()
    
    # Recent Orders
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    
    # Low Stock Alerts
    low_stock_items = get_low_stock_items()[:5]
    
    # Sales Chart Data (Last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_sales = db.session.query(
        func.date(Order.order_date).label('date'),
        func.sum(Order.total_amount).label('total')
    ).filter(Order.order_date >= seven_days_ago, Order.payment_status == 'Paid').group_by(func.date(Order.order_date)).all()
    
    sales_dates = [str(sale.date) for sale in daily_sales]
    sales_amounts = [float(sale.total) for sale in daily_sales]
    
    # Top Products with Revenue (Only Paid Orders)
    top_products = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_sold'),
        func.sum(OrderItem.subtotal).label('revenue')
    ).join(OrderItem).join(Order).filter(Order.payment_status == 'Paid').group_by(Product.id, Product.name).order_by(desc('revenue')).limit(5).all()
    
    return render_template('dashboard.html', title='Dashboard', 
                           total_sales=total_sales, 
                           pending_orders=pending_orders, 
                           low_stock_count=low_stock_count,
                           active_jobs=active_jobs,
                           recent_orders=recent_orders,
                           low_stock_items=low_stock_items,
                           sales_dates=sales_dates,
                           sales_amounts=sales_amounts,
                           top_products=top_products)

# ==================== INVENTORY ====================

@main_bp.route('/inventory')
@login_required
def inventory():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    query = Product.query
    
    if search:
        query = query.filter(
            (Product.name.contains(search)) | 
            (Product.sku.contains(search))
        )
    
    if category_filter:
        query = query.filter_by(category_id=category_filter)
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    categories = Category.query.all()
    
    # Get all product names for autocomplete
    all_product_names = [p.name for p in Product.query.with_entities(Product.name).all()]
    
    return render_template('inventory/list.html', products=products, 
                          categories=categories, search=search, 
                          category_filter=category_filter,
                          all_product_names=all_product_names)

@main_bp.route('/inventory/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def add_product():
    form = ProductForm()
    form.category_id.choices = [(0, 'Select Category')] + [(c.id, c.name) for c in Category.query.all()]
    form.supplier_id.choices = [(0, 'Select Supplier')] + [(s.id, s.name) for s in Supplier.query.all()]
    
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            # Ensure unique filename
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

        product = Product(
            sku=form.sku.data,
            name=form.name.data, 
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            description=form.description.data,
            cost_price=form.cost_price.data or 0,
            selling_price=form.selling_price.data,
            stock_quantity=form.stock_quantity.data,
            reorder_level=form.reorder_level.data,
            supplier_id=form.supplier_id.data if form.supplier_id.data != 0 else None,
            image_url=image_filename
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Product "{product.name}" added successfully!', 'success')
        return redirect(url_for('main.inventory'))
    
    # Get all product names for autocomplete
    all_product_names = [p.name for p in Product.query.with_entities(Product.name).all()]
    
    return render_template('inventory/form.html', form=form, title='Add Product', action='add', all_product_names=all_product_names)

@main_bp.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    form.category_id.choices = [(0, 'Select Category')] + [(c.id, c.name) for c in Category.query.all()]
    form.supplier_id.choices = [(0, 'Select Supplier')] + [(s.id, s.name) for s in Supplier.query.all()]
    
    if form.validate_on_submit():
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            product.image_url = filename

        product.sku = form.sku.data
        product.name = form.name.data
        product.category_id = form.category_id.data if form.category_id.data != 0 else None
        product.description = form.description.data
        product.cost_price = form.cost_price.data or 0
        product.selling_price = form.selling_price.data
        product.stock_quantity = form.stock_quantity.data
        product.reorder_level = form.reorder_level.data
        product.supplier_id = form.supplier_id.data if form.supplier_id.data != 0 else None
        
        db.session.commit()
        flash(f'Product "{product.name}" updated successfully!', 'success')
        return redirect(url_for('main.inventory'))
    
    all_product_names = [p.name for p in Product.query.with_entities(Product.name).all()]
    
    return render_template('inventory/form.html', form=form, title='Edit Product', action='edit', product=product, all_product_names=all_product_names)

@main_bp.route('/inventory/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_product(id):
    product = Product.query.get_or_404(id)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'Product "{name}" deleted successfully!', 'warning')
    return redirect(url_for('main.inventory'))

# ==================== ORDERS ====================

@main_bp.route('/orders')
@login_required
def orders():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = Order.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    orders = query.order_by(Order.order_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('orders/list.html', orders=orders, status_filter=status_filter)

@main_bp.route('/orders/create', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def create_order():
    form = OrderForm()
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.all()]
    
    if form.validate_on_submit():
        order = Order(
            customer_id=form.customer_id.data,
            status=form.status.data,
            payment_status=form.payment_status.data,
            payment_method=form.payment_method.data
        )
        db.session.add(order)
        db.session.commit()
        
        # Record transaction if paid
        if order.payment_status == 'Paid':
            txn = Transaction(
                type='Income',
                category='Sales',
                amount=order.total_amount,
                description=f'Order #{order.id} - {order.customer.name}',
                related_order_id=order.id
            )
            db.session.add(txn)
            db.session.commit()
        
        flash('Order created! Now add items.', 'success')
        return redirect(url_for('main.view_order', id=order.id))
    
    return render_template('orders/form.html', form=form, title='Create Order', action='create')

@main_bp.route('/orders/<int:id>')
@login_required
def view_order(id):
    order = Order.query.get_or_404(id)
    products = Product.query.filter(Product.stock_quantity > 0).all()
    return render_template('orders/view.html', order=order, products=products)

@main_bp.route('/orders/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def edit_order(id):
    order = Order.query.get_or_404(id)
    form = OrderForm(obj=order)
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.all()]
    
    if form.validate_on_submit():
        old_payment_status = order.payment_status
        order.customer_id = form.customer_id.data
        order.status = form.status.data
        order.payment_status = form.payment_status.data
        order.payment_method = form.payment_method.data
        
        # Record transaction if payment status changed to Paid
        if old_payment_status != 'Paid' and form.payment_status.data == 'Paid':
            txn = Transaction(
                type='Income',
                category='Sales',
                amount=order.total_amount,
                description=f'Order #{order.id} - Payment received',
                related_order_id=order.id
            )
            db.session.add(txn)
        
        db.session.commit()
        flash(f'Order #{order.id} updated successfully!', 'success')
        return redirect(url_for('main.view_order', id=order.id))
    
    return render_template('orders/form.html', form=form, title='Edit Order', action='edit', order=order)

@main_bp.route('/orders/<int:id>/add_item', methods=['POST'])
@login_required
@role_required('Admin', 'Staff')
def add_order_item(id):
    order = Order.query.get_or_404(id)
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    product = Product.query.get(product_id)
    if product:
        if product.stock_quantity < quantity:
            flash(f'Insufficient stock for {product.name}. Available: {product.stock_quantity}', 'danger')
        else:
            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.selling_price,
                subtotal=product.selling_price * quantity
            )
            db.session.add(item)
            
            # Update Order Total
            order.total_amount += item.subtotal
            
            # Deduct Stock
            product.stock_quantity -= quantity
            
            # Add Loyalty Points (1 point per PKR 100 spent)
            if order.customer:
                points_earned = int(item.subtotal / 100)
                order.customer.loyalty_points += points_earned
                if points_earned > 0:
                    flash(f'Customer earned {points_earned} loyalty points!', 'info')
            
            # Auto-update transaction if order is already paid
            if order.payment_status == 'Paid':
                existing_txn = Transaction.query.filter_by(related_order_id=order.id).first()
                if not existing_txn:
                    txn = Transaction(
                        type='Income',
                        category='Sales',
                        amount=order.total_amount,
                        description=f'Order #{order.id} - {order.customer.name}',
                        related_order_id=order.id
                    )
                    db.session.add(txn)
                else:
                    existing_txn.amount = order.total_amount
            
            db.session.commit()
            flash(f'{product.name} added to order.', 'success')
    
    return redirect(url_for('main.view_order', id=id))

@main_bp.route('/orders/<int:order_id>/remove_item/<int:item_id>', methods=['POST'])
@login_required
@role_required('Admin', 'Staff')
def remove_order_item(order_id, item_id):
    item = OrderItem.query.get_or_404(item_id)
    order = item.order
    
    # Restore stock
    product = item.product
    product.stock_quantity += item.quantity
    
    # Update order total
    order.total_amount -= item.subtotal
    
    # Update transaction if exists
    if order.payment_status == 'Paid':
        existing_txn = Transaction.query.filter_by(related_order_id=order.id).first()
        if existing_txn:
            existing_txn.amount = order.total_amount - item.subtotal
            if existing_txn.amount <= 0:
                db.session.delete(existing_txn)
    
    db.session.delete(item)
    db.session.commit()
    
    flash('Item removed from order.', 'info')
    return redirect(url_for('main.view_order', id=order_id))

@main_bp.route('/orders/<int:id>/invoice')
@login_required
def download_invoice(id):
    order = Order.query.get_or_404(id)
    pdf_buffer = generate_pdf_invoice(order)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f'invoice_{order.id}.pdf',
        mimetype='application/pdf'
    )

@main_bp.route('/orders/<int:id>/delete', methods=['POST'])
@login_required
@role_required('Admin')
def delete_order(id):
    order = Order.query.get_or_404(id)
    
    # Restore stock for all items
    for item in order.items:
        item.product.stock_quantity += item.quantity
    
    db.session.delete(order)
    db.session.commit()
    flash(f'Order #{id} deleted successfully!', 'warning')
    return redirect(url_for('main.orders'))

# ==================== CUSTOMERS ====================

@main_bp.route('/customers')
@login_required
def customers():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Customer.query
    
    if search:
        query = query.filter(
            (Customer.name.contains(search)) | 
            (Customer.phone.contains(search)) |
            (Customer.email.contains(search))
        )
    
    customers = query.order_by(Customer.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('customers/list.html', customers=customers, search=search)

@main_bp.route('/customers/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            name=form.name.data,
            phone=form.phone.data, 
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(customer)
        db.session.commit()
        flash(f'Customer "{customer.name}" added successfully!', 'success')
        return redirect(url_for('main.customers'))
    
    return render_template('customers/form.html', form=form, title='Add Customer', action='add')

@main_bp.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    form = CustomerForm(obj=customer)
    
    if form.validate_on_submit():
        customer.name = form.name.data
        customer.phone = form.phone.data
        customer.email = form.email.data
        customer.address = form.address.data
        
        db.session.commit()
        flash(f'Customer "{customer.name}" updated successfully!', 'success')
        return redirect(url_for('main.customers'))
    
    return render_template('customers/form.html', form=form, title='Edit Customer', action='edit', customer=customer)

@main_bp.route('/customers/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    name = customer.name
    db.session.delete(customer)
    db.session.commit()
    flash(f'Customer "{name}" deleted successfully!', 'warning')
    return redirect(url_for('main.customers'))

@main_bp.route('/customers/<int:id>')
@login_required
def view_customer(id):
    customer = Customer.query.get_or_404(id)
    orders = Order.query.filter_by(customer_id=id).order_by(Order.order_date.desc()).all()
    return render_template('customers/view.html', customer=customer, orders=orders)

# ==================== SUPPLIERS ====================

@main_bp.route('/suppliers')
@login_required
def suppliers():
    suppliers = Supplier.query.order_by(Supplier.created_at.desc()).all()
    return render_template('suppliers/list.html', suppliers=suppliers)

@main_bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def add_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data,
            contact_person=form.contact_person.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(supplier)
        db.session.commit()
        flash(f'Supplier "{supplier.name}" added successfully!', 'success')
        return redirect(url_for('main.suppliers'))
    
    return render_template('suppliers/form.html', form=form, title='Add Supplier', action='add')

@main_bp.route('/suppliers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=supplier)
    
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.contact_person = form.contact_person.data
        supplier.phone = form.phone.data
        supplier.email = form.email.data
        supplier.address = form.address.data
        
        db.session.commit()
        flash(f'Supplier "{supplier.name}" updated successfully!', 'success')
        return redirect(url_for('main.suppliers'))
    
    return render_template('suppliers/form.html', form=form, title='Edit Supplier', action='edit', supplier=supplier)

@main_bp.route('/suppliers/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    name = supplier.name
    db.session.delete(supplier)
    db.session.commit()
    flash(f'Supplier "{name}" deleted successfully!', 'warning')
    return redirect(url_for('main.suppliers'))

# ==================== PRODUCTION ====================

@main_bp.route('/production')
@login_required
def production():
    status_filter = request.args.get('status', '')
    
    query = ProductionJob.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    jobs = query.order_by(ProductionJob.start_date.desc()).all()
    
    return render_template('production/list.html', jobs=jobs, status_filter=status_filter, now=datetime.utcnow())

@main_bp.route('/production/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def add_job():
    form = ProductionJobForm()
    # Populate product choices
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]
    
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        job = ProductionJob(
            product_name=product.name, # Save name from selected product
            description=form.description.data,
            due_date=form.due_date.data,
            status=form.status.data,
            assigned_worker=form.assigned_worker.data
        )
        db.session.add(job)
        db.session.commit()
        flash(f'Production job for "{job.product_name}" created successfully!', 'success')
        return redirect(url_for('main.production'))
    
    return render_template('production/form.html', form=form, title='Create Job', action='add')

@main_bp.route('/production/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    job = ProductionJob.query.get_or_404(id)
    form = ProductionJobForm(obj=job)
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]
    
    # Set default product_id if not set (find product by name)
    if request.method == 'GET':
        product = Product.query.filter_by(name=job.product_name).first()
        if product:
            form.product_id.data = product.id
    
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        job.product_name = product.name
        job.description = form.description.data
        job.due_date = form.due_date.data
        job.status = form.status.data
        job.assigned_worker = form.assigned_worker.data
        
        db.session.commit()
        flash(f'Production job updated successfully!', 'success')
        return redirect(url_for('main.production'))
    
    return render_template('production/form.html', form=form, title='Edit Job', action='edit', job=job)

@main_bp.route('/production/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_job(id):
    job = ProductionJob.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('Production job deleted successfully!', 'warning')
    return redirect(url_for('main.production'))

# ==================== FINANCE ====================

@main_bp.route('/finance')
@login_required
def finance():
    page = request.args.get('page', 1, type=int)
    type_filter = request.args.get('type', '')
    
    query = Transaction.query
    
    if type_filter:
        query = query.filter_by(type=type_filter)
    
    transactions = query.order_by(Transaction.date.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    # Calculate totals
    total_income = db.session.query(func.sum(Transaction.amount)).filter_by(type='Income').scalar() or 0
    total_expense = db.session.query(func.sum(Transaction.amount)).filter_by(type='Expense').scalar() or 0
    net_profit = total_income - total_expense
    
    return render_template('finance/list.html', transactions=transactions, 
                          type_filter=type_filter,
                          total_income=total_income,
                          total_expense=total_expense,
                          net_profit=net_profit)

@main_bp.route('/finance/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Staff')
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        txn = Transaction(
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data,
            description=form.description.data
        )
        db.session.add(txn)
        db.session.commit()
        flash('Transaction recorded successfully!', 'success')
        return redirect(url_for('main.finance'))
    
    return render_template('finance/form.html', form=form, title='Record Transaction', action='add')

@main_bp.route('/finance/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def edit_transaction(id):
    txn = Transaction.query.get_or_404(id)
    form = TransactionForm(obj=txn)
    
    if form.validate_on_submit():
        txn.type = form.type.data
        txn.category = form.category.data
        txn.amount = form.amount.data
        txn.description = form.description.data
        
        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('main.finance'))
    
    return render_template('finance/form.html', form=form, title='Edit Transaction', action='edit', transaction=txn)

@main_bp.route('/finance/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_transaction(id):
    txn = Transaction.query.get_or_404(id)
    db.session.delete(txn)
    db.session.commit()
    flash('Transaction deleted successfully!', 'warning')
    return redirect(url_for('main.finance'))

# ==================== REPORTS ====================

@main_bp.route('/reports')
@login_required
def reports():
    # Sales data for chart (Last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    sales_data = db.session.query(
        func.date(Order.order_date).label('date'),
        func.sum(Order.total_amount).label('total')
    ).filter(Order.order_date >= thirty_days_ago, Order.payment_status == 'Paid').group_by(func.date(Order.order_date)).all()
    
    dates = [str(d.date) for d in sales_data]
    amounts = [float(d.total) for d in sales_data]
    
    # Top selling products (Revenue)
    top_products = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('quantity'),
        func.sum(OrderItem.subtotal).label('revenue')
    ).join(OrderItem).join(Order).filter(Order.payment_status == 'Paid').group_by(Product.id).order_by(desc('revenue')).limit(10).all()
    
    # Low stock items
    low_stock = get_low_stock_items()
    
    return render_template('reports/view.html', 
                          dates=dates, 
                          amounts=amounts,
                          top_products=top_products,
                          low_stock=low_stock)

@main_bp.route('/reports/export/products')
@login_required
def export_products():
    products = Product.query.all()
    data = [[p.sku, p.name, p.category.name if p.category else '', 
             p.stock_quantity, p.cost_price, p.selling_price] 
            for p in products]
    columns = ['SKU', 'Name', 'Category', 'Stock', 'Cost Price', 'Selling Price']
    
    buffer = export_to_excel(data, columns, 'products')
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='products_export.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@main_bp.route('/reports/export/orders')
@login_required
def export_orders():
    orders = Order.query.all()
    data = [[f'#{o.id}', o.order_date.strftime('%Y-%m-%d'), 
             o.customer.name if o.customer else '', 
             o.status, o.payment_status, o.total_amount] 
            for o in orders]
    columns = ['Order ID', 'Date', 'Customer', 'Status', 'Payment', 'Total']
    
    buffer = export_to_excel(data, columns, 'orders')
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='orders_export.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@main_bp.route('/reports/export/transactions')
@login_required
def export_transactions():
    transactions = Transaction.query.all()
    data = [[t.date.strftime('%Y-%m-%d'), t.type, t.category, 
             t.description, t.amount] 
            for t in transactions]
    columns = ['Date', 'Type', 'Category', 'Description', 'Amount']
    
    buffer = export_to_excel(data, columns, 'transactions')
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='transactions_export.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# ==================== SETTINGS ====================

@main_bp.route('/settings')
@login_required
@role_required('Admin')
def settings():
    users = User.query.all()
    categories = Category.query.all()
    return render_template('settings/index.html', users=users, categories=categories)

@main_bp.route('/settings/categories/add', methods=['POST'])
@login_required
@role_required('Admin')
def add_category():
    name = request.form.get('name')
    cat_type = request.form.get('type', 'Product')
    
    category = Category(name=name, type=cat_type)
    db.session.add(category)
    db.session.commit()
    
    flash(f'Category "{name}" added successfully!', 'success')
    return redirect(url_for('main.settings'))

@main_bp.route('/settings/categories/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_category(id):
    category = Category.query.get_or_404(id)
    name = category.name
    db.session.delete(category)
    db.session.commit()
    flash(f'Category "{name}" deleted successfully!', 'warning')
    return redirect(url_for('main.settings'))

@main_bp.route('/settings/change-password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    from app.utils import log_action
    user = User.query.get_or_404(user_id)
    
    # Only allow users to change their own password, or admin to change any password
    if current_user.id != user_id and current_user.role != 'Admin':
        abort(403)
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verify current password (unless admin changing someone else's password)
        if current_user.id == user_id:
            if not user.check_password(current_password):
                flash('Current password is incorrect!', 'danger')
                return redirect(url_for('main.change_password', user_id=user_id))
        
        # Validate new password
        if len(new_password) < 8:
            flash('New password must be at least 8 characters long!', 'danger')
            return redirect(url_for('main.change_password', user_id=user_id))
        
        if new_password != confirm_password:
            flash('New passwords do not match!', 'danger')
            return redirect(url_for('main.change_password', user_id=user_id))
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        # Log the action
        log_action(
            action=f'Changed password for user: {user.username}',
            entity_type='User',
            entity_id=user.id,
            details=f'Password changed by {current_user.username}'
        )
        
        flash(f'Password for {user.username} updated successfully!', 'success')
        
        if current_user.role == 'Admin':
            return redirect(url_for('main.settings'))
        else:
            return redirect(url_for('main.index'))
    
    return render_template('settings/change_password.html', user=user)

@main_bp.route('/settings/audit-log')
@login_required
@role_required('Admin')
def audit_log():
    from app.models import AuditLog
    page = request.args.get('page', 1, type=int)
    user_filter = request.args.get('user', '')
    action_filter = request.args.get('action', '')
    
    query = AuditLog.query
    
    if user_filter:
        query = query.filter(AuditLog.username.contains(user_filter))
    
    if action_filter:
        query = query.filter(AuditLog.action.contains(action_filter))
    
    logs = query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('settings/audit_log.html', logs=logs, 
                          user_filter=user_filter, action_filter=action_filter)


# ==================== DATABASE INITIALIZATION (ONE-TIME USE) ====================

@main_bp.route('/init-database-secret-2024')
def init_database():
    """
    One-time database initialization endpoint for free tier users.
    Visit this URL once after setting up PostgreSQL to initialize the database.
    """
    try:
        # Check if database is already initialized
        existing_users = User.query.count()
        if existing_users > 0:
            return """
            <html>
            <head><title>Database Already Initialized</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: #28a745;">✅ Database Already Initialized!</h1>
                <p>Your database already contains data.</p>
                <p><strong>Users found:</strong> """ + str(existing_users) + """</p>
                <p><a href="/" style="color: #007bff; text-decoration: none; font-size: 18px;">Go to Login →</a></p>
            </body>
            </html>
            """
        
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create Admin User
        admin = User(username='admin', email='admin@newpindi.com', role='Admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create Staff User
        staff = User(username='staff', email='staff@newpindi.com', role='Staff')
        staff.set_password('staff123')
        db.session.add(staff)
        
        # Create Categories
        cat1 = Category(name='Sofas', type='Product')
        cat2 = Category(name='Beds', type='Product')
        cat3 = Category(name='Tables', type='Product')
        cat4 = Category(name='Wood', type='Material')
        cat5 = Category(name='Fabric', type='Material')
        db.session.add_all([cat1, cat2, cat3, cat4, cat5])
        db.session.commit()
        
        # Create Suppliers
        sup1 = Supplier(name='Wood Suppliers Ltd', contact_person='Ahmed Khan', 
                        phone='0300-1234567', email='ahmed@woodsuppliers.com',
                        address='Industrial Area, Rawalpindi')
        sup2 = Supplier(name='Fabric House', contact_person='Sara Ali', 
                        phone='0321-9876543', email='sara@fabrichouse.com',
                        address='Saddar, Rawalpindi')
        db.session.add_all([sup1, sup2])
        db.session.commit()
        
        # Create Customers
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
        txn1 = Transaction(type='Income', category='Sales',
                          amount=45000, description='Order #1 - 3-Seater Sofa',
                          related_order_id=order1.id,
                          date=datetime.utcnow() - timedelta(days=5))
        
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
        
        return """
        <html>
        <head><title>Database Initialized Successfully</title></head>
        <body style="font-family: Arial; padding: 50px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h1 style="font-size: 48px;">🎉 Database Initialized Successfully!</h1>
            <div style="background: white; color: #333; padding: 30px; border-radius: 16px; max-width: 600px; margin: 30px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
                <h2 style="color: #28a745;">✅ All Set!</h2>
                <p style="font-size: 18px;">Your PostgreSQL database has been initialized with:</p>
                <ul style="text-align: left; font-size: 16px; line-height: 2;">
                    <li>✅ 2 Users (admin & staff)</li>
                    <li>✅ 5 Categories</li>
                    <li>✅ 2 Suppliers</li>
                    <li>✅ 3 Customers</li>
                    <li>✅ 5 Products</li>
                    <li>✅ 3 Sample Orders</li>
                    <li>✅ 3 Production Jobs</li>
                    <li>✅ 5 Transactions</li>
                </ul>
                <hr style="margin: 20px 0;">
                <h3 style="color: #007bff;">Login Credentials:</h3>
                <p style="font-size: 16px;"><strong>Admin:</strong> username: <code>admin</code> | password: <code>admin123</code></p>
                <p style="font-size: 16px;"><strong>Staff:</strong> username: <code>staff</code> | password: <code>staff123</code></p>
                <hr style="margin: 20px 0;">
                <p style="color: #dc3545; font-weight: bold;">⚠️ IMPORTANT: Change these passwords immediately after logging in!</p>
                <a href="/login" style="display: inline-block; margin-top: 20px; padding: 15px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: bold;">Go to Login →</a>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"""
        <html>
        <head><title>Database Initialization Error</title></head>
        <body style="font-family: Arial; padding: 50px; text-align: center;">
            <h1 style="color: #dc3545;">❌ Error Initializing Database</h1>
            <p style="font-size: 18px; color: #666;">An error occurred:</p>
            <pre style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: left; max-width: 800px; margin: 20px auto; overflow-x: auto;">{str(e)}</pre>
            <p><a href="/" style="color: #007bff; text-decoration: none; font-size: 18px;">Go Back →</a></p>
        </body>
        </html>
        """

