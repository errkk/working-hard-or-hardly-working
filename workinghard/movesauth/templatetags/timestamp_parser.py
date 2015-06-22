from dateutil import parser

from django import template

register = template.Library()


@register.filter('datestring_to_time')
def convert_datestring_to_time(datestring):
    return parser.parse(datestring)
