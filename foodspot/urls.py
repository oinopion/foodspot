from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'foodspot.views.home_page', name='home'),
    url(r'^texts/', include('foodspot.texts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
