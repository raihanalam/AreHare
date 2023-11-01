from django import template

register = template.Library()

def range_filter(value):
     return value[0:60]+'...'

def range_filter_lg(value):
     return value[0:200]+'...'

register.filter('range_filter',range_filter)
register.filter('range_filter_lg',range_filter_lg)