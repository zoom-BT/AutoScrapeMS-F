from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    email1 = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nom d\'utilisateur')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EmailForm(forms.Form):
    email = forms.EmailField(label='Votre adresse e-mail', max_length=100)

class ScrapeForm(forms.Form):
    urls = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Entrez les URLs séparés par des virgules'}),
        label="URLs à scraper",
        help_text="Saisissez les URLs des sites web à scraper, séparés par des virgules."
    )
    emails = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Entrez les emails séparés par des virgules'}),
        label="Adresses Email",
        help_text="Saisissez les adresses email séparées par des virgules."
    )
    schedule_interval = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Intervalle en minutes'}),
        label="Intervalle de scraping (en minutes)",
        required=False,
        help_text="Laisser vide pour démarrer immédiatement"
    )


