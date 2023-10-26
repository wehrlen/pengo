from django import template


register = template.Library()


@register.filter
def status_label(value):
    value = value.lower()  
    if value == 'online':
        return 'en ligne'
    elif value == 'offline':
        return 'hors ligne'
    elif value == 'idle':
        return 'inactif'
    elif value == 'dnd':
        return 'npd'
    else:
        return value 