from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ArticleForm
from .models import Article, ArticleRating, Category

from django.contrib.auth.models import User
from django.db.models import Avg




@login_required
def pending_articles(request):

    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("article_list")

    articles = Article.objects.filter(
        status="pending"
    ).select_related(
        "author",
        "category"
    ).order_by("-created_at")

    return render(request, "article/pending_articles.html", {
        "articles": articles
    })


@login_required
def approve_article(request, article_id):

    if not (
        request.user.is_staff
        or request.user.is_superuser
    ):
        return redirect("article_list")

    article = get_object_or_404(
        Article,
        id=article_id,
        status="pending"
    )

    if request.method == "POST":
        article.status = "published"
        article.save()

    return redirect("pending_articles")

def article_list(request):
    articles = (
        Article.objects
        .filter(status="published")
        .select_related("author", "category")
        .prefetch_related(
            "ratings",
            "likes",
            "dislikes",
            "favorites",
        )
        .order_by("-created_at")
    )

    return render(request, "article/article_list.html", {
        "articles": articles
    })


def article_detail(request, article_id):

    article = get_object_or_404(
        Article.objects
        .filter(
            id=article_id
        )
        .select_related(
            "author",
            "category"
        )
        .prefetch_related(
            "ratings",
            "likes",
            "dislikes",
            "favorites"
        )
        .annotate(
            average_rating=Avg("ratings__value")
        )
    )
    if article.status == "pending":

        if not (
            request.user.is_authenticated
            and (
                request.user == article.author
                or request.user.is_staff
                or request.user.is_superuser
            )
        ):
            return redirect("article_list")

    return render(
        request,
        "article/article_detail.html",
        {
            "article": article
        }
    )
@login_required
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            article = form.save(commit=False)

            article.author = request.user
            article.status = "pending"

            article.save()

            return redirect(
                "article_detail",
                article_id=article.id
            )

    else:
        form = ArticleForm()

    return render(request, "article/article_create.html", {
        "form": form
    })


@login_required
def article_edit(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )


    if not (
        request.user.is_superuser
        or request.user.is_staff
        or article.author == request.user
    ):
        return redirect(
            "article_detail",
            article_id=article.id
        )

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            request.FILES,
            instance=article
        )

        if form.is_valid():
            article = form.save(commit=False)

            # Every edit needs admin approval again
            article.status = "pending"

            article.save()

            return redirect(
                "article_detail",
                article_id=article.id
            )

    else:
        form = ArticleForm(
            instance=article
        )

    return render(request, "article/article_edit.html", {
        "form": form,
        "article": article
    })


@login_required
def article_delete(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )

    if not (
        request.user.is_superuser
        or request.user.is_staff
        or article.author == request.user
    ):
        return redirect(
            "article_detail",
            article_id=article.id
        )

    if request.method == "POST":
        article.delete()

        return redirect("article_list")

    return render(request, "article/article_delete.html", {
        "article": article
    })


@login_required
def article_like(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.user in article.likes.all():


        article.likes.remove(request.user)

    else:
        article.likes.add(request.user)

        article.dislikes.remove(request.user)

    return redirect(
        "article_detail",
        article_id=article.id
    )


@login_required
def article_dislike(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.user in article.dislikes.all():

        article.dislikes.remove(request.user)

    else:

        article.dislikes.add(request.user)

        article.likes.remove(request.user)

    return redirect(
        "article_detail",
        article_id=article.id
    )


@login_required
def article_favorite(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.user in article.favorites.all():

        article.favorites.remove(request.user)

    else:

        article.favorites.add(request.user)

    return redirect(
        "article_detail",
        article_id=article.id
    )


@login_required
def article_rate(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.method == "POST":

        rating_value = request.POST.get("rating")

        if rating_value and rating_value.isdigit():

            rating_value = int(rating_value)

            if 1 <= rating_value <= 5:

                ArticleRating.objects.update_or_create(
                    article=article,
                    user=request.user,
                    defaults={
                        "value": rating_value
                    }
                )

    return redirect(
        "article_detail",
        article_id=article.id
    )
def popular_articles(request):

    articles = Article.objects.filter(
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
    )

    return render(
        request,
        "article/popular_articles.html",
        {
            "articles": articles
        }
    )

def category_list(request):
    categories = Category.objects.all().order_by("name")

    return render(request, "article/category_list.html", {
        "categories": categories
    })


def category_articles(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id
    )

    articles = Article.objects.filter(
        category=category,
        status="published"
    ).select_related(
        "author",
        "category"
    ).prefetch_related(
        "ratings",
        "likes",
        "dislikes",
        "favorites"
    ).order_by("-created_at")

    return render(request, "article/category_articles.html", {
        "category": category,
        "articles": articles
    })

def author_list(request):
    authors = User.objects.filter(
        articles__status="published"
    ).distinct().order_by("username")

    return render(request, "article/author_list.html", {
        "authors": authors
    })


def author_articles(request, author_id):
    author = get_object_or_404(
        User,
        id=author_id
    )

    articles = Article.objects.filter(
        author=author,
        status="published"
    ).select_related(
        "author",
        "category"
    ).prefetch_related(
        "ratings",
        "likes",
        "dislikes",
        "favorites"
    ).order_by("-created_at")

    return render(request, "article/author_articles.html", {
        "author": author,
        "articles": articles
    })

@login_required
def favorite_articles(request):
    articles = Article.objects.filter(
        favorites=request.user,
        status="published"
    ).select_related(
        "author",
        "category"
    ).prefetch_related(
        "ratings",
        "likes",
        "dislikes",
        "favorites"
    ).order_by("-created_at")

    return render(request, "article/favorite_articles.html", {
        "articles": articles
    })