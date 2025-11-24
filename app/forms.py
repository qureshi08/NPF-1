from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, FloatField, IntegerField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProductForm(FlaskForm):
    sku = StringField('SKU', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    description = TextAreaField('Description')
    cost_price = FloatField('Cost Price', validators=[Optional()])
    selling_price = FloatField('Selling Price', validators=[DataRequired()])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired()])
    reorder_level = IntegerField('Reorder Level', default=5)
    supplier_id = SelectField('Supplier', coerce=int, validators=[Optional()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])

class OrderForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending')
    payment_status = SelectField('Payment Status', choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid'), ('Refunded', 'Refunded')], default='Unpaid')
    payment_method = SelectField('Payment Method', choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Bank Transfer', 'Bank Transfer')], default='Cash')

class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address')

class SupplierForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address')

class TransactionForm(FlaskForm):
    type = SelectField('Type', choices=[('Income', 'Income'), ('Expense', 'Expense')], validators=[DataRequired()])
    category = SelectField('Category', choices=[('Sales', 'Sales'), ('Rent', 'Rent'), ('Salaries', 'Salaries'), ('Utilities', 'Utilities'), ('Inventory', 'Inventory'), ('Other', 'Other')], validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    description = TextAreaField('Description')

class ProductionJobForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due Date', validators=[Optional()])
    status = SelectField('Status', choices=[('Queued', 'Queued'), ('Cutting', 'Cutting'), ('Assembling', 'Assembling'), ('Polishing', 'Polishing'), ('Finished', 'Finished')], default='Queued')
    assigned_worker = StringField('Assigned Worker')
