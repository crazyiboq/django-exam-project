from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.db.models import Avg

from articles.models import Article


def home(request):

    popular_articles = Article.objects.filter(
        status="published"
    ).annotate(
        average_rating=Avg("ratings__value")
    ).filter(
        average_rating__gte=4
    ).select_related(
        "author",
        "category"
    ).prefetch_related(
        "ratings",
        "likes",
        "dislikes",
        "favorites"
    ).order_by(
        "-average_rating",
        "-created_at"
    )[:3]

    return render(request, "home.html", {
        "popular_articles": popular_articles
    })


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("articles/", include("articles.urls")),
    path("", home, name="home"),
]