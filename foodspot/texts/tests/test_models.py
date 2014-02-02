import time
from unittest import mock
from django.shortcuts import resolve_url
from django.test import TestCase
from django.utils import baseconv
from ..models import Article, ONE_DAY


class ArticleTest(TestCase):
    def test_get_absolute_url_published(self):
        article = Article(slug='spam-eggs', status=Article.STATUS.published)
        expected = resolve_url('article_detail', slug='spam-eggs')
        self.assertEqual(expected, article.get_absolute_url())

    def test_get_absolute_url_draft(self):
        article = Article(pk=1, slug='spam-eggs', status=Article.STATUS.draft)
        signature = article.signed_id()
        expected = resolve_url(
            'article_preview', slug='spam-eggs', signature=signature)
        self.assertEqual(expected, article.get_absolute_url())

    def test_signed_id(self):
        article = Article(pk=1, slug='spam-eggs')
        signed_id = article.signed_id()
        self.assertEqual(str(article.pk), signed_id[0])

    def test_is_signed_id(self):
        article = Article(pk=1, slug='spam-eggs')
        self.assertFalse(article.is_signed_id("1"))

        signed_id = article.signed_id()
        self.assertTrue(article.is_signed_id(signed_id))

    def test_is_published(self):
        article = Article(status=Article.STATUS.published)
        self.assertTrue(article.is_published)

    def test_stale_signature(self):
        article = Article(pk=1, slug='spam-eggs')
        yesterday = time.time() - ONE_DAY.total_seconds() - 1
        with mock.patch.object(article.signer, 'timestamp') as timestamp:
            timestamp.return_value = self.encode_timestamp(yesterday)
            signature = article.signed_id()
        self.assertFalse(article.is_signed_id(signature))

    def encode_timestamp(self, timestamp):
        return baseconv.base62.encode(int(timestamp))

