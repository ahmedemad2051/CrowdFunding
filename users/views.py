from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from projects.models import Image, Project, Comment, Donation
from django.contrib import messages


# Create your views here.
@login_required
def profile(request):
    context = {}

    user_projects = Project.objects.filter(owner=request.user)  # get user projects
    donations = Project.objects.filter(donations__user=request.user)  # get user projects
    context['user_projects'] = user_projects
    context['donations'] = donations

    return render(request, "users/profile.html", context)

@login_required
def delete_profile(request):

    if request.method == "GET":
        print("User deleted")
        request.user.delete()
        messages.success(request , "You just deleted your account successfully ..")

    return redirect("/")
