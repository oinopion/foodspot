from django import template
from django.test import TestCase


class MarkdownTest(TestCase):
    def test_fails_silently(self):
        html = self.render("{% markdown article.text %}", {})
        self.assertEqual("", html)

    def render(self, template_text, context):
        t = template.Template("{% load markdown_tags %}" + template_text)
        c = template.Context(context)
        return t.render(c)
