from django.test import TestCase
from .factories import ArticleFactory, PublishedArticleFactory, DraftArticleFactory


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

