from django.shortcuts import render, redirect
from .forms import UserRegisterationForm
from django.contrib import messages
#from django.core.mail import send_mail
#from crowd_funding import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    return Response("Email account is activated")


def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()

            # # Send Confirmation Email
            # subject = "Confirm Your Email"
            # message = "Thank you for registering in our website, please click link below to confirm your email.\n"
            # from_email = settings.EMAIL_HOST_USER
            # to_list = [request.POST['email'], from_email]
            # send_mail(subject, message, from_email, to_list, fail_silently=True)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterationForm()
    return render(request, 'registration/register.html', {'form': form})



