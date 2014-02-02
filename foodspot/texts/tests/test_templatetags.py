import re
from django import template
from django.test import TestCase
from ..templatetags.markdown_tags import InstagramPattern


class MarkdownTest(TestCase):
    def test_fails_silently(self):
        html = self.render("{% markdown article.text %}", {})
        self.assertEqual("", html)

    def test_has_instagram_extension(self):
        text = "[instagram:hello]"
        html = self.render("{% markdown text %}", {'text': text})
        self.assertIn('instagram.com/p/hello/media', html)

    def render(self, template_text, context):
        t = template.Template("{% load markdown_tags %}" + template_text)
        c = template.Context(context)
        return t.render(c)


class InstagramPatternTest(TestCase):
    regexp = re.compile(InstagramPattern.PATTERN)

    def test_regexp(self):
        self.assertRegex('[instagram:abc]', self.regexp)
        self.assertRegex('[instagram:yiuh1y]', self.regexp)
        self.assertNotRegex('[instagram:]', self.regexp)
        self.assertNotRegex('![link](http://example.com)', self.regexp)

    def test_handle_match(self):
        pattern = InstagramPattern()
        match = self.regexp.match('[instagram:hello]')
        element = pattern.handleMatch(match)
        self.assertEqual('img', element.tag)
        self.assertEqual('instagram', element.attrib.get('class'))
        self.assertEqual(
            '//instagram.com/p/hello/media/?size=l',
            element.get('src')
        )