from django import template

register = template.Library()

@register.filter
def sum_prices(items):
    total_price = 0
    for item in items:
        if item.product.type == 'Headphones':
            total_price += item.product.headphones.price * item.quantity
        elif item.product.type == 'Mouse':
            total_price += item.product.mouse.price * item.quantity
        elif item.product.type == 'Keyboard':
            total_price += item.product.keyboard.price * item.quantity
    return round(total_price,2)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def number(string):
    return float(string)

@register.filter
def sort_carts(array):
    return array.order_by('updated')