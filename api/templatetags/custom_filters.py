from django import template

register = template.Library()

@register.filter
def format_price(obj):
    if hasattr(obj, 'currency'):
        return f"{obj.price / 100:.2f} {obj.currency.upper()}"
    return "0.00 USD"  # По умолчанию, если объект не подходит