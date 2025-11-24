"""
Quick fix script to create a working admin user
"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Delete existing admin
    existing = User.query.filter_by(username='admin').first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
    
    # Create new admin with proper password
    admin = User()
    admin.username = 'admin'
    admin.email = 'admin@newpindi.com'
    admin.role = 'Admin'
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    
    # Test the password
    test_user = User.query.filter_by(username='admin').first()
    if test_user and test_user.check_password('admin123'):
        print("[OK] Admin user created successfully!")
        print("[OK] Password verification works!")
        print("\nLogin with:")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("[ERROR] Password verification failed!")
