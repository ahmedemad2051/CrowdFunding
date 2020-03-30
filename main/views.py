from django.shortcuts import render
from projects.models import Project
from django.shortcuts import render, get_object_or_404, redirect
from projects.forms import ProjectForm, ImageForm
from django.http import HttpResponse
from django.forms import modelformset_factory
from projects.models import Image, Project
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum
from decimal import Decimal

# Create your views here.

def index(req):
    selectedProjects = Project.objects.filter(active=True) [:6]
    latestProjects = Project.objects.order_by('-created_at') 


    context={
               "selectedProjects":selectedProjects,
               "latestProjects": latestProjects
    }

    return render(req, "main/index.html", {"context": context})


