# -*- coding:utf-8 -*-
__version__ = '1.0.0.0'

import json
from django import template

register = template.Library()


@register.filter(name='format_none')  
def format_none(value):  
    if not value:
        return ''
    return value


@register.filter(name="cut")
def cut(value, arg=80):
    value = value.replace("<br></br>", "")
    value = value.replace("&nbsp;", "")
    if len(value) > arg:
        return " %s......" % value[:arg]
    else:
        return value


@register.filter(name="strtojson")
def strtojson(str_arg):
    return json.loads(str_arg)


@register.filter(name="inttolist")
def inttolist(int_arg):
    return range(1, int_arg)


@register.filter('strftime')
def strftime(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")


@register.filter('commentcount')
def commentcount(queryset):
    return len(queryset)
