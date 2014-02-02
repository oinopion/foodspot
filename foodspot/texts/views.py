from django.http import Http404
from django.views.generic import DetailView, ListView
from .models import Article


class ArticleView(DetailView):
    queryset = Article.published.all()
    context_object_name = 'article'


class ArticleListView(ListView):
    queryset = Article.published.all()
    context_object_name = 'articles'


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


article_list = ArticleListView.as_view()
article_detail = ArticleView.as_view()
article_preview = ArticlePreviewView.as_view()
