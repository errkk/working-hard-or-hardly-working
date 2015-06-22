from datetime import datetime
from dateutil import parser

from django import template

register = template.Library()


@register.filter('datestring_to_time')
def convert_datestring_to_time(datestring):
    return parser.parse(datestring)


@register.filter('datestring_to_date')
def convert_datestring_to_date(datestring):
    return datetime.strptime(datestring, '%Y%m%d')
