from django.urls import path

from . import views


urlpatterns = [

# =========================
# MAIN ARTICLE PAGES
# =========================

path(
    "",
    views.article_list,
    name="article_list"
),

path(
    "popular/",
    views.popular_articles,
    name="popular_articles"
),

path(
    "categories/",
    views.category_list,
    name="category_list"
),

path(
    "categories/<int:category_id>/",
    views.category_articles,
    name="category_articles"
),

path(
    "authors/",
    views.author_list,
    name="author_list"
),

path(
    "authors/<int:author_id>/",
    views.author_articles,
    name="author_articles"
),

path(
    "favorites/",
    views.favorite_articles,
    name="favorite_articles"
),

path(
    "create/",
    views.article_create,
    name="article_create"
),

path(
    "pending/",
    views.pending_articles,
    name="pending_articles"
),
    # =========================
    # ARTICLE DETAIL
    # =========================

    path(
        "<int:article_id>/",
        views.article_detail,
        name="article_detail"
    ),


    # =========================
    # ARTICLE MANAGEMENT
    # =========================

    path(
        "<int:article_id>/edit/",
        views.article_edit,
        name="article_edit"
    ),

    path(
        "<int:article_id>/delete/",
        views.article_delete,
        name="article_delete"
    ),

    path(
        "<int:article_id>/approve/",
        views.approve_article,
        name="approve_article"
    ),


    # =========================
    # ARTICLE INTERACTIONS
    # =========================

    path(
        "<int:article_id>/like/",
        views.article_like,
        name="article_like"
    ),

    path(
        "<int:article_id>/dislike/",
        views.article_dislike,
        name="article_dislike"
    ),

    path(
        "<int:article_id>/favorite/",
        views.article_favorite,
        name="article_favorite"
    ),

    path(
        "<int:article_id>/rate/",
        views.article_rate,
        name="article_rate"
    ),
]