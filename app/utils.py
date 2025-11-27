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
    """Generate beautiful, professional PDF invoice for an order"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.pdfgen import canvas
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*cm, bottomMargin=1*cm, leftMargin=1.5*cm, rightMargin=1.5*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    company_name_style = ParagraphStyle(
        'CompanyName',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#1a1f2e'),
        spaceAfter=3,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=36
    )
    
    company_tagline_style = ParagraphStyle(
        'CompanyTagline',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#667eea'),
        alignment=TA_LEFT,
        spaceAfter=5,
        fontName='Helvetica-Oblique'
    )
    
    company_info_style = ParagraphStyle(
        'CompanyInfo',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        alignment=TA_LEFT,
        spaceAfter=20
    )
    
    invoice_title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=5,
        alignment=TA_RIGHT,
        fontName='Helvetica-Bold'
    )
    
    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1a1f2e'),
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=12
    )
    
    # Header with Company Info and Invoice Title
    header_data = [
        [
            Paragraph("<b>NEW PINDI FURNITURE</b>", company_name_style),
            Paragraph("INVOICE", invoice_title_style)
        ],
        [
            Paragraph("Premium Furniture Solutions", company_tagline_style),
            ''
        ],
        [
            Paragraph("Rawalpindi, Pakistan<br/>Phone: +92-XXX-XXXXXXX<br/>Email: info@newpindifurniture.com", company_info_style),
            ''
        ]
    ]
    
    header_table = Table(header_data, colWidths=[10*cm, 8*cm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Colored separator line
    separator_data = [['']]
    separator_table = Table(separator_data, colWidths=[18*cm])
    separator_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 3, colors.HexColor('#667eea')),
    ]))
    elements.append(separator_table)
    elements.append(Spacer(1, 0.6*cm))
    
    # Invoice Details and Customer Info
    info_data = [
        [
            Paragraph("<b>INVOICE DETAILS</b>", section_header_style),
            '',
            Paragraph("<b>BILL TO</b>", section_header_style)
        ],
        [
            Paragraph(f"<b>Invoice Number:</b> INV-{order.id:05d}", styles['Normal']),
            '',
            Paragraph(f"<b>{order.customer.name if order.customer else 'Walk-in Customer'}</b>", styles['Normal'])
        ],
        [
            Paragraph(f"<b>Date:</b> {order.order_date.strftime('%d %B, %Y')}", styles['Normal']),
            '',
            Paragraph(f"{order.customer.phone if order.customer else 'N/A'}", styles['Normal'])
        ],
        [
            Paragraph(f"<b>Status:</b> <font color='#28a745'>{order.status}</font>", styles['Normal']),
            '',
            Paragraph(f"{order.customer.address if order.customer and order.customer.address else ''}", styles['Normal'])
        ],
        [
            Paragraph(f"<b>Payment:</b> <font color='{'#28a745' if order.payment_status == 'Paid' else '#ffc107'}'>{order.payment_status}</font>", styles['Normal']),
            '',
            Paragraph(f"{order.customer.email if order.customer and order.customer.email else ''}", styles['Normal'])
        ],
    ]
    
    info_table = Table(info_data, colWidths=[6*cm, 1*cm, 11*cm])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.8*cm))
    
    # Items Table
    items_data = [['#', 'ITEM DESCRIPTION', 'QTY', 'UNIT PRICE', 'AMOUNT']]
    
    # Add items
    for idx, item in enumerate(order.items, 1):
        items_data.append([
            str(idx),
            item.product.name,
            str(item.quantity),
            f'PKR {item.unit_price:,.0f}',
            f'PKR {item.subtotal:,.0f}'
        ])
    
    # Calculate totals
    subtotal = order.total_amount
    tax = 0
    total = subtotal + tax
    
    # Add spacing row
    items_data.append(['', '', '', '', ''])
    
    # Add summary rows
    items_data.append(['', '', '', 'Subtotal:', f'PKR {subtotal:,.0f}'])
    items_data.append(['', '', '', 'Tax (0%):', f'PKR {tax:,.0f}'])
    items_data.append(['', '', '', 'TOTAL:', f'PKR {total:,.0f}'])
    
    items_table = Table(items_data, colWidths=[1*cm, 9*cm, 2*cm, 3*cm, 3*cm])
    items_table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 14),
        ('TOPPADDING', (0, 0), (-1, 0), 14),
        
        # Items styling
        ('ALIGN', (0, 1), (0, -5), 'CENTER'),
        ('ALIGN', (2, 1), (2, -5), 'CENTER'),
        ('ALIGN', (3, 1), (-1, -5), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -5), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -5), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -5), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -5), 0.5, colors.HexColor('#dee2e6')),
        ('TOPPADDING', (0, 1), (-1, -5), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -5), 10),
        
        # Summary section styling
        ('ALIGN', (3, -3), (-1, -1), 'RIGHT'),
        ('FONTNAME', (3, -3), (-1, -2), 'Helvetica'),
        ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (3, -3), (-1, -2), 11),
        ('FONTSIZE', (3, -1), (-1, -1), 14),
        ('TEXTCOLOR', (3, -1), (-1, -1), colors.HexColor('#667eea')),
        ('LINEABOVE', (3, -3), (-1, -3), 1, colors.HexColor('#dee2e6')),
        ('LINEABOVE', (3, -1), (-1, -1), 2.5, colors.HexColor('#667eea')),
        ('TOPPADDING', (3, -1), (-1, -1), 12),
        ('BOTTOMPADDING', (3, -1), (-1, -1), 12),
        ('BACKGROUND', (3, -1), (-1, -1), colors.HexColor('#f0f4ff')),
    ]))
    elements.append(items_table)
    
    # Payment Information
    elements.append(Spacer(1, 1*cm))
    
    payment_info_style = ParagraphStyle(
        'PaymentInfo',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#555555'),
        alignment=TA_LEFT,
        spaceAfter=5,
        leading=12
    )
    
    payment_box_data = [[
        Paragraph("<b>PAYMENT INFORMATION</b>", section_header_style)
    ], [
        Paragraph(
            "Bank: Allied Bank Limited<br/>"
            "Account Title: New Pindi Furniture<br/>"
            "Account Number: XXXX-XXXX-XXXX-XXXX<br/>"
            "IBAN: PK XX XXXX XXXX XXXX XXXX XXXX XXXX",
            payment_info_style
        )
    ]]
    
    payment_box = Table(payment_box_data, colWidths=[18*cm])
    payment_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
    ]))
    elements.append(payment_box)
    
    # Footer
    elements.append(Spacer(1, 1*cm))
    
    footer_thank_you_style = ParagraphStyle(
        'FooterThankYou',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#667eea'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=8
    )
    
    footer_contact_style = ParagraphStyle(
        'FooterContact',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=5
    )
    
    elements.append(Paragraph("Thank you for your business!", footer_thank_you_style))
    elements.append(Paragraph("For any queries, please contact us at info@newpindifurniture.com or call +92-XXX-XXXXXXX", footer_contact_style))
    elements.append(Paragraph("This is a computer-generated invoice and does not require a signature.", footer_contact_style))
    
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

