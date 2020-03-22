from django.shortcuts import render


# Create your views here.

def index(req):
    return render(req, "projects/index.html")


def show(req, project_id):
    return render(req, "projects/show.html")


def create(req):
    return render(req, "projects/create.html")
