# Manual UI Updates Needed

## 1. Add Analytics Link to Sidebar (base.html)

**Location:** `app/templates/base.html` - After line 170 (after Reports link)

**Add this line:**
```html
        <a href="{{ url_for('main.analytics') }}" class="{{ 'active' if 'analytics' in request.endpoint else '' }}"><i class="fas fa-chart-pie me-2"></i> Analytics</a>
```

**Full context (lines 169-172 should become):**
```html
        <a href="{{ url_for('main.reports') }}" class="{{ 'active' if 'report' in request.endpoint else '' }}"><i
                class="fas fa-file-alt me-2"></i> Reports</a>
        <a href="{{ url_for('main.analytics') }}" class="{{ 'active' if 'analytics' in request.endpoint else '' }}"><i
                class="fas fa-chart-pie me-2"></i> Analytics</a>
        {% if current_user.role == 'Admin' %}
```

---

## 2. Payment Form Already Created!

The payment form UI is in `app/templates/orders/payments.html` - it's ready!

But we need to add a "Record Payment" button to the order view page.

---

## 3. Global Search Bar (Coming Next)

Will add a search input in the top navigation bar.

---

For now, you can test:
- Analytics: Visit `/analytics` directly
- Payments: Visit `/orders/1/payments` directly
- Search: Visit `/search?q=test` directly
