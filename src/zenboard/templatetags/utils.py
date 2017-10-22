"""
Zenboard utils template tags
"""
from django import template

import zenboard


register = template.Library()


@register.simple_tag
def zenboard_version():
    """Helper template tag that return current Zenboard version"""
    return zenboard.__version__
