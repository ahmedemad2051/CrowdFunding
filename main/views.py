from django.shortcuts import render
from django.db.models import Q
from projects.models import Project, Category
from django.http import HttpResponse
from decimal import Decimal
from django.http import JsonResponse

# Create your views here.



def index(req):
    selectedProjects = Project.objects.filter(active=True, enable=True)[:6]
    latestProjects = Project.objects.filter(enable=True).order_by('-created_at')[:5]

    top_rated = Project.objects.filter(ratings__isnull=False).order_by('ratings__average')[:5]
    categories = Category.objects.all()
    counter = 0
    custom_categories = []
    row = []
    for category in categories:
        print(counter)
        row.append(category)
        counter += 1
        if counter % 4 == 0 or categories.count() == counter:
            custom_categories.append(row)
            row = []

    print(custom_categories)
    context = {
            "selectedProjects": selectedProjects,
            "latestProjects": latestProjects,
            'top_rated': top_rated,
            'categories': custom_categories,

        }

    return render(req, "main/index.html", {"context": context})


def contact(request):
    return render(request, "main/contact.html")

# def search(request):
#     query = request.GET.get('q')
#     results = Project.objects.filter(Q(title__icontains=query) | Q(tags__icontains=query))
#
#     return render(request, "projects/index.html", {"results": results})
