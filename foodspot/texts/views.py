from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import YearArchiveView

from .models import Article


@cache_control(max_age=60 * 5, public=True)
def article_detail(request, slug):
    article = get_object_or_404(Article.published, slug=slug)
    return render_article(article, 'texts/article_detail.html', {
        'article': article,
    })


@never_cache
def article_preview(request, slug, signature):
    article = get_object_or_404(Article.objects, slug=slug)
    if not article.is_signed_id(signature):
        raise Http404('Provided signature is not valid')
    return render_article(article, 'texts/article_detail.html', {
        'article': article,
    })


class ArticlesByYearView(YearArchiveView):
    queryset = Article.published.all()
    context_object_name = 'articles'
    make_object_list = True
    date_field = 'created'

    def get_year(self):
        try:
            return super().get_year()
        except Http404:
            now = timezone.now()
            return str(now.year)


article_by_year = ArticlesByYearView.as_view()


def render_article(article, template_name, context):
    key = '%s|%s' % (article.cache_key(), template_name)
    content = cache.get(key)
    if not content:
        content = render_to_string(template_name, context)
        cache.set(key, content)
    return HttpResponse(content)
