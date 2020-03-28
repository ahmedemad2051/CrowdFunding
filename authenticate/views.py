from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterationForm


# Create your views here.
def login(req):
    return render(req, "authenticate/login.html")


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