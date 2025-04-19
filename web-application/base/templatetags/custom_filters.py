from django import template

register = template.Library()

@register.filter
def sum_prices(items):
    total_price = 0
    for item in items:
        total_price += item.price * item.quantity
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
def sort_orders(array):
    return array.order_by('updated_at')

@register.filter
def module(number):
    return number%10