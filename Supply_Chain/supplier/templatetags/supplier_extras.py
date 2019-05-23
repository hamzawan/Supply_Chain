from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price
