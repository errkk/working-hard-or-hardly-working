<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> cc8a1fb414cb8c97e7404c03ddfbc05c909bfcee
from dateutil import parser

from django import template

register = template.Library()


@register.filter('datestring_to_time')
def convert_datestring_to_time(datestring):
    return parser.parse(datestring)
<<<<<<< HEAD


@register.filter('datestring_to_date')
def convert_datestring_to_date(datestring):
    return datetime.strptime(datestring, '%Y%m%d')
=======
>>>>>>> cc8a1fb414cb8c97e7404c03ddfbc05c909bfcee
