import hurl

urlpatterns = hurl.patterns('foodspot.texts.views', {
    '': 'article_by_year',
    '<slug>': 'article_detail',
    '<slug>/<signature:str>': 'article_preview',
})
