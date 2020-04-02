from django.shortcuts import render
from django.db.models import Q
from projects.models import Project, Category


# Create your views here.

def index(req):
    selectedProjects = Project.objects.filter(active=True, enable=True)[:6]
    latestProjects = Project.objects.filter(enable=True).order_by('-created_at')[:5]
    top_rated = Project.objects.filter(ratings__isnull=False).order_by('ratings__average')[:5]
    categories = Category.objects.all()

    context = {
        "selectedProjects": selectedProjects,
        "latestProjects": latestProjects,
        'top_rated': top_rated,
        'categories': categories,

    }

    return render(req, "main/index.html", {"context": context})


def contact(request):
    return render(request, "main/contact.html")

# def search(request):
#     query = request.GET.get('q')
#     results = Project.objects.filter(Q(title__icontains=query) | Q(tags__icontains=query))
#
#     return render(request, "projects/index.html", {"results": results})
