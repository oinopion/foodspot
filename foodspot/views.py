from django.shortcuts import render
from foodspot.texts.models import Article


def home_page(request):
    latest_articles = Article.published.all()[:5]
    return render(request, 'home.html', {
        'latest_articles': latest_articles
    })
