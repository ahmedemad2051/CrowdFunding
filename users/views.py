from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Image, Project, Comment

# Create your views here.
def profile(req):
    return render(req, "users/profile.html")

@login_required
def display_user_projects(request):
    context = {}
    user_projects = Project.objects.filter(owner = request.user) # get user projects
    context['user_projects'] = user_projects
    return render(request, "users/profile", context)