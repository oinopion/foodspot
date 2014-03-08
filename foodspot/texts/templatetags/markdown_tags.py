import markdown
from django import template
from markdown.util import etree
from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension

register = template.Library()


@register.simple_tag(name='markdown')
def render_markdown(text):
    return markdown.markdown(text, extensions=[InstagramExtension()])


class InstagramPattern(Pattern):
    REDIRECT_URL = 'https://instagram.com/p/%s/media/?size=l'
    PATTERN = r'\[instagram:(?P<id>[^\]]+)\]'

    def __init__(self, markdown_instance=None):
        super().__init__(self.PATTERN, markdown_instance)

    def handleMatch(self, m):
        href = self.REDIRECT_URL % m.group('id')
        return etree.Element('img', attrib={'src': href, 'class': 'instagram'})


class InstagramExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('instagram', InstagramPattern(md), '_begin')
