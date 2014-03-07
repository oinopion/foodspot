from django import forms
from django.db import models
from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    list_display = ('id', 'title', 'slug', 'status', 'created', 'modified')
    list_display_links = ('id', 'title', 'slug')
    list_filter = ('status',)
    search_fields = ('title', 'slug')
    readonly_fields = ('status_changed', 'modified')
    fields = (
        'title', 'status', 'slug', 'created', 'excerpt', 'text',
        'status_changed', 'modified',
    )
    actions = ['publish_articles']
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'rows': 30, 'cols': 80})
        },
    }

    def publish_articles(self, request, queryset):
        count = queryset.count()
        if count > 40:
            msg = 'Please select less than 20 posts (%d were selected).'
            self.message_user(request, msg % count)
            return
        for article in queryset:
            article.publish()
        self.message_user(request, 'Published articles: %d' % count)
    publish_articles.short_description = 'Mark selected articles as published'


admin.site.register(Article, ArticleAdmin)
