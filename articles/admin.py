from django.contrib import admin
from .models import Category, SubCategory, Article, Comment
from markdownx.admin import MarkdownxModelAdmin

# Inline for Comments under an Article
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ['user', 'content']


# Admin for Article
@admin.register(Article)
class ArticleAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'author', 'category', 'subcategory', 'slug')
    list_filter = ('category', 'subcategory', 'author')
    search_fields = ('title', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]


# Admin for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# Admin for SubCategory
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# Admin for Comment (optional - for standalone comment editing)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'content')
    search_fields = ('user__email', 'article__title', 'content')
    list_filter = ('article', 'user')
