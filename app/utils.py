from functools import wraps
from flask import abort
from flask_login import current_user
import io
from datetime import datetime
import pandas as pd

def role_required(*roles):
    """Decorator to require specific roles for routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def generate_pdf_invoice(order):
    """Generate beautiful PDF invoice for an order"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.pdfgen import canvas
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CompanyTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=5,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    invoice_title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading2'],
        fontSize=20,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Header
    elements.append(Paragraph("NEW PINDI FURNITURE", title_style))
    elements.append(Paragraph("Rawalpindi, Pakistan | Phone: +92-XXX-XXXXXXX", subtitle_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # Invoice Title with colored background
    elements.append(Paragraph("INVOICE", invoice_title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Invoice Info and Customer Info side by side
    info_data = [
        ['Invoice Number:', f'INV-{order.id:05d}', '', 'Bill To:'],
        ['Date:', order.order_date.strftime('%d %B, %Y'), '', order.customer.name if order.customer else 'Walk-in Customer'],
        ['Status:', order.status, '', order.customer.phone if order.customer else ''],
        ['Payment:', order.payment_status, '', order.customer.address if order.customer and order.customer.address else ''],
    ]
    
    info_table = Table(info_data, colWidths=[2.5*cm, 5*cm, 1*cm, 8*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (3, 0), (3, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
        ('TEXTCOLOR', (3, 0), (3, 0), colors.HexColor('#555555')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Items Table Header
    items_data = [['#', 'Item Description', 'Qty', 'Unit Price (PKR)', 'Amount (PKR)']]
    
    # Items
    for idx, item in enumerate(order.items, 1):
        items_data.append([
            str(idx),
            item.product.name,
            str(item.quantity),
            f'{item.unit_price:,.0f}',
            f'{item.subtotal:,.0f}'
        ])
    
    # Subtotal, Tax, Total
    items_data.append(['', '', '', '', ''])  # Empty row
    items_data.append(['', '', '', 'Subtotal:', f'{order.total_amount:,.0f}'])
    items_data.append(['', '', '', 'Tax (0%):', '0'])
    items_data.append(['', '', '', 'Total Amount:', f'{order.total_amount:,.0f}'])
    
    items_table = Table(items_data, colWidths=[1*cm, 8*cm, 1.5*cm, 3.5*cm, 3.5*cm])
    items_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Items
        ('ALIGN', (0, 1), (0, -5), 'CENTER'),
        ('ALIGN', (2, 1), (2, -5), 'CENTER'),
        ('ALIGN', (3, 1), (-1, -5), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -5), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -5), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -5), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -5), 0.5, colors.HexColor('#dee2e6')),
        
        # Totals
        ('ALIGN', (3, -3), (-1, -1), 'RIGHT'),
        ('FONTNAME', (3, -3), (-1, -2), 'Helvetica'),
        ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (3, -3), (-1, -1), 11),
        ('TEXTCOLOR', (3, -1), (-1, -1), colors.HexColor('#0d6efd')),
        ('LINEABOVE', (3, -3), (-1, -3), 1, colors.HexColor('#dee2e6')),
        ('LINEABOVE', (3, -1), (-1, -1), 2, colors.HexColor('#0d6efd')),
        ('TOPPADDING', (3, -1), (-1, -1), 10),
        ('BOTTOMPADDING', (3, -1), (-1, -1), 10),
    ]))
    elements.append(items_table)
    
    # Footer
    elements.append(Spacer(1, 1*cm))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph("<b>Thank you for your business!</b>", footer_style))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("For any queries, please contact us at info@newpindifurniture.com", footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def export_to_excel(data, columns, filename):
    """Export data to Excel file"""
    df = pd.DataFrame(data, columns=columns)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    buffer.seek(0)
    return buffer

def export_to_csv(data, columns):
    """Export data to CSV"""
    df = pd.DataFrame(data, columns=columns)
    return df.to_csv(index=False)

def get_low_stock_items():
    """Get products with stock below reorder level"""
    from app.models import Product
    return Product.query.filter(Product.stock_quantity <= Product.reorder_level).all()

def calculate_profit_margin(cost_price, selling_price):
    """Calculate profit margin percentage"""
    if cost_price == 0:
        return 0
    return ((selling_price - cost_price) / cost_price) * 100

def format_currency(amount):
    """Format amount as PKR currency"""
    return f"PKR {amount:,.0f}"

def log_action(action, entity_type=None, entity_id=None, details=None):
    """Log user action to audit log"""
    from app.models import AuditLog
    from app import db
    from flask import request
    from flask_login import current_user
    
    try:
        log = AuditLog(
            user_id=current_user.id if current_user.is_authenticated else None,
            username=current_user.username if current_user.is_authenticated else 'Anonymous',
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=request.remote_addr if request else None
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        # Don't fail the main operation if logging fails
        print(f"Audit log error: {e}")
        db.session.rollback()

def send_notification(message, user_id=None, type='info', link=None):
    """
    Send a notification to a specific user or all admins (if user_id is None).
    """
    from app.models import Notification, User
    from app import db
    
    try:
        if user_id:
            # Send to specific user
            notif = Notification(user_id=user_id, message=message, type=type, link=link)
            db.session.add(notif)
        else:
            # Send to all Admins
            admins = User.query.filter_by(role='Admin').all()
            for admin in admins:
                notif = Notification(user_id=admin.id, message=message, type=type, link=link)
                db.session.add(notif)
        
        db.session.commit()
    except Exception as e:
        print(f"Notification error: {e}")
        db.session.rollback()

