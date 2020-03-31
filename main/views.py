from django.shortcuts import render
from projects.models import Project


# Create your views here.

def index(req):
    selectedProjects = Project.objects.filter(active=True)[:6]
    latestProjects = Project.objects.order_by('-created_at')[:5]

    context = {
        "selectedProjects": selectedProjects,
        "latestProjects": latestProjects
    }
    return render(req, "main/index.html", {"context": context})


def contact(request):
    return render(request, "main/contact.html")
