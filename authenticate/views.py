from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
# def login_user(request):
#     if request.POST:
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             if request.POST.get('next'):
#                 return HttpResponseRedirect(request.POST.get('next'))
#             return HttpResponseRedirect("/")
#         else:
#             # Return an 'invalid login' error message.
#             messages.error(request, "Credentials Error, please try again!")
#     return redirect(to="login")


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
    return render(request, 'registration/register.html', {'form': form})



