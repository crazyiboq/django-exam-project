from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) < 3:
            raise forms.ValidationError(
                "Username must be at least 3 characters long."
            )

        if not username.isalnum():
            raise forms.ValidationError(
                "Username can only contain letters and numbers."
            )

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        max_length=150,
        required=False
    )

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "bio",
            "profile_picture",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Tell us a little about yourself..."
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")

        super().__init__(*args, **kwargs)

        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name
        self.fields["email"].initial = self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)

        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]

        if commit:
            self.user.save()
            profile.save()

        return profile