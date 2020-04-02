from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegisterationForm
from django.contrib import messages
from django.core.mail import send_mail
from crowd_funding import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from authenticate.models import Activation
import datetime
from django.http import HttpResponse

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
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            token = get_random_string(length=32)
            Activation.objects.create(token=token, user=new_user)
            # Send Confirmation Email
            subject = "Confirm Your Email"
            message = f'''
                Thank you for registering in our website,
                please click link below to confirm your email.
                http://localhost:8000/auth/activate/{token}
            '''

            from_email = settings.EMAIL_HOST_USER
            to_list = [request.POST['email'], from_email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            username = form.cleaned_data.get('username')
            messages.success(request,
                             f'Account created for {username}!,Please check your email to activate your account first')
            return redirect('home')
    else:
        form = UserRegisterationForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(req, token):
    activation = get_object_or_404(Activation, token=token)
    is_valid = (timezone.now() - activation.created_at) < datetime.timedelta(hours=24)
    if is_valid and not activation.is_used:
        activation.is_used = True
        activation.save()
        activation.user.is_active = True
        activation.user.save()
        messages.success(req, "Congrats, Your account activated successfully")
    else:
        messages.error(req, "Sorry, your activation token is not valid OR used before,Please try to send it again")
    return redirect("login")
