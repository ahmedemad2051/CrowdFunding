from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    last_name = forms.CharField(required=True, max_length=50)
    profile_picture = forms.ImageField(required=False)

    # TO-DO: enhance these fields
    mobile = forms.CharField(required=False, max_length=20)
    # activate
    # created_at

    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'profile_picture', 'password1', 'password2']
