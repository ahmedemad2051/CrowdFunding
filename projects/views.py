from django.shortcuts import render, get_object_or_404
from projects.forms import ProjectForm, ImageForm
from django.http import HttpResponse
from django.forms import modelformset_factory
from projects.models import Image, Project
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.

def index(req):
    context = {}
    projects = Project.objects.all()
    context['projects'] = projects
    return render(req, "projects/index.html", context)


def show(req, project_slug):
    context = {}
    project = Project.objects.get(slug=project_slug)
    similar_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project.id)
    context['project'] = project
    context['similar_projects'] = similar_projects
    return render(req, "projects/show.html", context)


@login_required
def create(req):
    context = {}
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)
    if req.method == "POST":
        projectForm = ProjectForm(req.POST)
        formset = ImageFormSet(req.POST, req.FILES,
                               queryset=Image.objects.none())
        if projectForm.is_valid() and formset.is_valid():
            project = projectForm.save(commit=False)
            project.owner = req.user
            project.save()
            projectForm.save_m2m()
            for image in req.FILES.getlist('form-0-image'):
                # for img in image_list:
                photo = Image(project=project, image=image)
                photo.save()

            messages.success(req,
                             "Campaign Created Successfully!")
            return HttpResponseRedirect("/")
    else:
        projectForm = ProjectForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    context['form'] = projectForm
    context['formset'] = formset
    return render(req, "projects/create.html", context)
