from django.shortcuts import render
from projects.models import Project

# Create your views here.

def index(req):
    selectedProjects = Project.objects.filter(active=True)
    lp = Project.objects.order_by('-created_at')

    context={
               "selectedProjects":selectedProjects,
               "lp": lp
    }

    return render(req, "main/index.html", {"context": context})


