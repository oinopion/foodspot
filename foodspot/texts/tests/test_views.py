from unittest import mock
from django.test import TestCase
from .factories import ArticleFactory, PublishedArticleFactory, DraftArticleFactory
from foodspot.texts.views import ArticleListView


class ArticleViewTest(TestCase):
    def url(self, article):
        return '/texts/%s/' % article.slug

    def test_renders_template(self):
        article = PublishedArticleFactory.create()
        resp = self.client.get(self.url(article))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'texts/article_detail.html')
        self.assertIn('article', resp.context)

    def test_does_not_show_drafts(self):
        article = ArticleFactory.create()
        resp = self.client.get(self.url(article))
        self.assertEqual(404, resp.status_code)


class ArticleListViewTest(TestCase):
    def url(self):
        return '/texts/'

    def test_renders_template(self):
        PublishedArticleFactory.create()
        resp = self.client.get(self.url())
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'texts/article_list.html')
        self.assertIn('articles', resp.context)

    def test_does_not_contain_drafts(self):
        draft = ArticleFactory.create()
        published = PublishedArticleFactory()
        resp = self.client.get(self.url())
        self.assertContains(resp, published.title)
        self.assertNotContains(resp, draft.title)

    def test_limits_posts(self):
        PublishedArticleFactory.create_batch(2)
        with mock.patch.object(ArticleListView, 'paginate_by', 1):
            resp = self.client.get(self.url())
        self.assertEqual(1, len(resp.context['articles']))


class ArticlePreviewViewTest(TestCase):
    def url(self, article, signature=None):
        signature = signature or article.signed_id()
        return '/texts/%s/%s/' % (article.slug, signature)

    def test_renders_template(self):
        article = DraftArticleFactory.create()
        resp = self.client.get(self.url(article))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'texts/article_detail.html')
        self.assertIn('article', resp.context)

    def test_404_for_bad_signature(self):
        article = DraftArticleFactory.create()
        resp = self.client.get(self.url(article, 'bad-signature'))
        self.assertEqual(404, resp.status_code)

