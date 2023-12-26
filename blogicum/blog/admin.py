from django.contrib import admin

from .models import Category, Location, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category'
    )
    list_per_page = 10
    list_editable = (
        'is_published',
    )
    list_display_links = None


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'title',
        'description',
        'slug'
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'name'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'text',
        'author',
        'post'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
