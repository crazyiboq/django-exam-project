from django.contrib import admin
from .models import Article, ArticleRating, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "content",
        "author__username",
    )

    list_filter = (
        "category",
        "created_at",
        "updated_at",
    )


@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "user",
        "value",
    )

    list_filter = ("value",)