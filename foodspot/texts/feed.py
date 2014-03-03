from datetime import timedelta
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy
from django.views.decorators.cache import cache_page
from .models import Article


class LatestArticleFeed(Feed):
    title = ugettext_lazy("Page title")
    description = ugettext_lazy("Page blurb")
    link = reverse_lazy('home')
    items_limit = 20
    ttl = 120

    description_template = 'texts/feed_description.html'

    def items(self):
        return Article.published.all().order_by('-created')[:self.items_limit]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.modified

cache_for_two_hours = cache_page(timedelta(hours=2).total_seconds())
latest_articles_feed = cache_for_two_hours(LatestArticleFeed())
