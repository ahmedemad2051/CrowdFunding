from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Image, Project, Comment, Donation
from users.models import Account
from .forms import UserRegisterationForm
from django.contrib import messages


# Create your views here.
@login_required
def profile(request):
    context = {}

    user_projects = Project.objects.filter(owner=request.user)  # get user projects
    donations = Project.objects.filter(donations__user=request.user)  # get user projects

    user_obj = Account.objects.get(email=request.user)
    user = UserRegisterationForm(request.POST or None, instance=user_obj)
    if request.POST:
        if user.is_valid():
            user.save()
            messages.success(request, "Profile Updated Successfully!")
        else:
            messages.error(request, "Failed to update profile!")

    context['user_projects'] = user_projects
    context['donations'] = donations
    context['user'] = user
    context['email'] = request.user
    return render(request, "users/profile.html", context)


@login_required
def delete_profile(request):

    if request.method == "GET":
        print("User deleted")
        request.user.delete()
        messages.success(request , "You just deleted your account successfully ..")

    return redirect("/")

