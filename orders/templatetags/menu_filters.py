from django import template

register = template.Library()

@register.filter
def to_image(name):
    # "COFFEE/காபி" → "coffee.jpeg" or "placeholder.jpeg" if empty
    english = name.split('/')[0].strip().lower()
    return english + '.jpeg' if english else 'placeholder.jpeg'

@register.filter
def tamil_name(name):
    # "COFFEE/காபி" → "காபி"
    parts = name.split('/')
    return parts[1].strip() if len(parts) > 1 else name

@register.filter
def to_english(name):
    # "COFFEE/காபி" → "Coffee"
    parts = name.split('/')
    return parts[0].strip().title()