from django.contrib import admin

from .models import Article, Category, ArticleRating


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
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
        "author__username",
    )

    actions = (
        "publish_articles",
        "set_pending",
    )

    @admin.action(description="Approve selected articles")
    def publish_articles(self, request, queryset):
        queryset.update(status="published")

    @admin.action(description="Set selected articles as pending")
    def set_pending(self, request, queryset):
        queryset.update(status="pending")


@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "user",
        "value",
    )