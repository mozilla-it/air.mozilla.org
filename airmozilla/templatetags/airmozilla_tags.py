from django import template
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.html import format_html
from django.utils.formats import date_format

register = template.Library()


@register.filter
def relativedate(d):
    return format_html(
        '<time datetime="{iso}" title="{human}">{relative}</time>',
        iso=d.isoformat(),
        relative=naturaltime(d),
        human=date_format(d, 'DATETIME_FORMAT'),
    )
