from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def format_float(context, *args):
    """ To use this tag, put {% load frontend_extras %} in your template. """
    value = args[0]
    trailing_numbers = args[1]
    return "{0:.{1}f}".format(value, trailing_numbers)
    # surveys = context['surveys']
    # enrollment = kwargs['enrollment']
    # return [i for i in enrollment if i in surveys]


@register.simple_tag(takes_context=True)
def format_weight(context, *args):
        amount = args[0]
        if amount < 1.0:
            format = "{0:.0f}{1}".format(amount * 1000, "g")
        else:
            format = "{0:.2f}{1}".format(amount, "kg")
        return format


@register.simple_tag(takes_context=True)
def format_volume(context, *args, unit="l"):
    volume = args[0]
    # unit = args[1]
    return "{0:.2f}{1}".format(volume, unit)


@register.simple_tag(takes_context=True)
def format_time(context, *args):
    time = args[0]
    if time < 24 * 60:
        format = "{0:.0f}{1}".format(time, "min")
    else:
        format = "{0:.0f}{1}".format(time / (24 * 60), "days")
    return format