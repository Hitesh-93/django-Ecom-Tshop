from django import template
from math import floor


register = template.Library()

@register.filter
def rupee(number):
    return f'₹ {number}'

@register.simple_tag
def min_price(tshirt):
    size = tshirt.sizevarient_set.all().order_by('price').first()
    return floor(size.price)


@register.simple_tag
def sale_price(tshirt):
    price = min_price(tshirt)
    discount = tshirt.discount
    return floor(price - (price * (discount / 100)))


@register.simple_tag
def get_active_size_btn_class(active_size, size):
    if active_size == size:
        return "btn-dark"
    else:
        return "btn-light"
    