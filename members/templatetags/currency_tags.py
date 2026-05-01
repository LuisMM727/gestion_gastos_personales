from django import template

register = template.Library()


@register.filter
def gs_format(value):
    try:
        # Convierte a entero para quitar decimales y formatea con puntos
        return "{:,.0f}".format(float(value)).replace(",", ".")
    except (ValueError, TypeError):
        return value
