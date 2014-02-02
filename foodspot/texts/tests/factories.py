# encoding: utf-8
import factory
from .. import models


class ArticleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Article

    title = factory.Sequence('Article {}'.format)
    slug = factory.Sequence('article-{}'.format)
    text = """
# Hello, World!
## Fun with Chech language

Nechť již hříšné saxofony ďáblů rozzvučí síň úděsnými tóny waltzu, tanga a
quickstepu. Ó, náhlý déšť teď zvířil prach a čilá laň běží s houfcem gazel k
úkrytům. Hleď, toť přízračný kůň v mátožné póze šíleně úpí.
"""


class PublishedArticleFactory(ArticleFactory):
    status = models.Article.STATUS.published


class DraftArticleFactory(ArticleFactory):
    status = models.Article.STATUS.draft
