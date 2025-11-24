from app import create_app, db
from app.models import User, Customer, Supplier, Category, Product, Order, OrderItem, ProductionJob, Transaction

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Customer': Customer,
        'Supplier': Supplier,
        'Category': Category,
        'Product': Product,
        'Order': Order,
        'OrderItem': OrderItem,
        'ProductionJob': ProductionJob,
        'Transaction': Transaction
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
