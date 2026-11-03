from django.contrib import admin
from .models import Post, User, Category, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    list_filter = ('categories', 'author')
    search_fields = ('title', 'content', 'author_username')
    ordering = ('id',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author_username', 'post_title')
    ordering = ('created_at',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)