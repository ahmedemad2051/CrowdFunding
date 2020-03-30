from django.shortcuts import render, redirect
from .forms import UserRegisterationForm
from django.contrib import messages
from django.core.mail import send_mail
from crowd_funding import settings


def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()

            # Send Confirmation Email
            subject = "Confirm Your Email"
            message = "Thank you for registering in our website, please click link below to confirm your email.\n"
            from_email = settings.EMAIL_HOST_USER
            to_list = [request.POST['email']]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterationForm()
    return render(request, 'registration/register.html', {'form': form})



