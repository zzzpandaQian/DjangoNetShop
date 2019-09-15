from django.template import Library

register = Library()

@register.filter
def sum_price(value,count):
    return int(value) * int(count)