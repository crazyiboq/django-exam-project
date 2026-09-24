from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(
        max_length=200
    )

    image = models.ImageField(
        upload_to="articles/",
        blank=True,
        null=True
    )

    content = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("published", "Published"),
        ],
        default="pending"
    )

    likes = models.ManyToManyField(
        User,
        related_name="liked_articles",
        blank=True
    )

    dislikes = models.ManyToManyField(
        User,
        related_name="disliked_articles",
        blank=True
    )

    favorites = models.ManyToManyField(
        User,
        related_name="favorite_articles",
        blank=True
    )

    def average_rating(self):

        result = self.ratings.aggregate(
            average=Avg("value")
        )["average"]

        return result or 0

    def __str__(self):
        return self.title


class ArticleRating(models.Model):

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    value = models.PositiveSmallIntegerField()

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["article", "user"],
                name="unique_article_rating"
            )
        ]

    def __str__(self):
        return f"{self.article.title} - {self.value}"