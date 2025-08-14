from django import template

register = template.Library()

@register.filter
def naira(value):
    """Format a number as Nigerian Naira with proper formatting"""
    try:
        # Convert to float and format with thousand separators
        amount = float(value)
        # Format with commas and remove unnecessary decimal places
        if amount == int(amount):
            return f"₦{int(amount):,}"
        else:
            return f"₦{amount:,.2f}"
    except (ValueError, TypeError):
        return f"₦{value}"
