from django.conf import settings
from django.http import Http404
from django.utils import timezone
from django.views.generic import DetailView, ListView, YearArchiveView
from .models import Article


class ArticleListView(ListView):
    queryset = Article.published.all()
    context_object_name = 'articles'
    paginate_by = settings.MAX_ARTICLES_PER_PAGE


class ArticlesByYearView(YearArchiveView):
    queryset = Article.published.all()
    context_object_name = 'articles'
    template_name_suffix = '_list'
    make_object_list = True
    date_field = 'created'

    def get_year(self):
        try:
            return super().get_year()
        except Http404:
            now = timezone.now()
            return str(now.year)


class ArticleView(DetailView):
    queryset = Article.published.all()
    context_object_name = 'article'


class ArticlePreviewView(DetailView):
    queryset = Article.objects.all()
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = super().get_object(queryset=queryset)
        if not article.is_signed_id(self.signature):
            raise Http404('Provided signature is not valid')
        return article

    @property
    def signature(self):
        return self.kwargs.get('signature', '')


article_list = ArticlesByYearView.as_view()
article_detail = ArticleView.as_view()
article_preview = ArticlePreviewView.as_view()
