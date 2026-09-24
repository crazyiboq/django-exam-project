from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "image",
            "content",
            "category",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter article title..."
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "rows": 12,
                    "placeholder": "Write your article here..."
                }
            ),
        }