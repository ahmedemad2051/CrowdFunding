from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Image, Project, Comment, Donation


# Create your views here.
@login_required
def profile(request):
    context = {}
    user_projects = Project.objects.filter(owner = request.user) # get user projects
    # user_donations = Donation.objects.filter(project = request.user)
    # print(user_donations)
    context['user_projects'] = user_projects
    # context['user_donations'] = user_donations

    return render(request, "users/profile.html", context)

