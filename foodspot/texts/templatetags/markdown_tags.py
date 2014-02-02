import markdown
from django import template

register = template.Library()


@register.simple_tag(name='markdown')
def render_markdown(text):
    return markdown.markdown(text)
