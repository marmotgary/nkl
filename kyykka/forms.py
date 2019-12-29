from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    player_number = forms.IntegerField( min_value=0, max_value=99)
    username = forms.EmailField(label='Email', max_length=254)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'player_number', 'first_name', 'last_name', 'password1', 'password2', )
