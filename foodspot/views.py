from django.views.decorators.cache import cache_control
from foodspot.texts.models import Article
from foodspot.texts.views import render_articles


@cache_control(max_age=60 * 5, public=True)
def home_page(request):
    latest_articles = Article.published.all()[:5]
    return render_articles(latest_articles, 'home.html', {
        'latest_articles': latest_articles,
    })
