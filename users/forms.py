from django import forms
from django.core.validators import RegexValidator

from users.models import Account
from django.contrib.auth.forms import UserCreationForm


class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    profile_picture = forms.ImageField(required=False)
    # '^[\+02]?(01)(0|1|2|5)([0-9]{8})$'
    phone_regex = RegexValidator(regex=r'^[\+02]?(01)(0|1|2|5)([0-9]{8})$',
                                 message="Egyptian Phone numbers are only allowed.")
    mobile = forms.CharField(validators=[phone_regex], max_length=14, required=False)  # validators should be a list

    facebook = forms.CharField(required=False, max_length=200)
    instagram = forms.CharField(required=False, max_length=200)
    twitter = forms.CharField(required=False, max_length=200)
    public_info = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'username', 'mobile', 'profile_picture',
                  'facebook', 'instagram', 'twitter', 'public_info', 'password1', 'password2']
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'profile_picture': 'Profile Picture',
        }
