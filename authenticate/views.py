from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

@login_required
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        render(request, "home.html")
    else:
        # Return an 'invalid login' error message.
        render(request, "/")