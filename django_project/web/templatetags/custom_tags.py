from django.template import Library


register = Library()


@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given
    numerical value.
    """
    return range(value)
