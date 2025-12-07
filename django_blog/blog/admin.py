from .models import Post, Comment
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')


admin.site.site_header = "Django Blog Administration"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'post__title')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
