import hurl

urlpatterns = hurl.patterns('foodspot.texts.views', {
    '': 'article_list',
    '<slug>': 'article_detail',
    '<slug>/<signature:str>': 'article_preview',
})
