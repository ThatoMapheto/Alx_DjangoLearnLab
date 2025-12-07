from django.contrib import admin
from .models import Post, Comment
from taggit.models import Tag  # Import Tag from taggit

# Unregister the default Tag model from taggit if it's registered
# Then register it with custom admin if needed
try:
    admin.site.unregister(Tag)
except admin.sites.NotRegistered:
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author', 'tags')
    search_fields = ('title', 'content')
    filter_horizontal = ()

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'post__title')
