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
    fields = ('title', 'status', 'slug', 'created', 'text', 'status_changed', 'modified')


admin.site.register(Article, ArticleAdmin)
