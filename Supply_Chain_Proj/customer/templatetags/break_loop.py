from django import template

register = template.Library()

@register.filter('break')
def break_(loop):
    raise StopLoopException(loop, False)
