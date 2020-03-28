from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
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


def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterationForm()
    return render(request, 'authenticate/register.html', {'form': form})
