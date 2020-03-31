from django.shortcuts import render
from django.db.models import Q
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


def search(request):

    query = request.GET.get('q')
    results = Project.objects.filter(Q(title__icontains=query) | Q(tags__icontains=query))



    return render(request, "projects/index.html", {"results": results})
