from django.shortcuts import render
from projects.forms import ProjectForm, ImageForm
from django.http import HttpResponse
from django.forms import modelformset_factory
from projects.models import Image, Project
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.

def index(req):
    return render(req, "projects/index.html")


def show(req, project_id):
    return render(req, "projects/show.html")


def create(req):
    # print(Project.objects.first().images.all())
    context = {}
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)
    if req.method == "POST":
        projectForm = ProjectForm(req.POST)
        formset = ImageFormSet(req.POST, req.FILES,
                               queryset=Image.objects.none())
        if projectForm.is_valid() and formset.is_valid():
            project_form = projectForm.save(commit=False)
            # project_form.user = req.user
            project_form.save()
            for image in req.FILES.getlist('form-0-image'):
                # for img in image_list:
                photo = Image(project=project_form, image=image)
                photo.save()

            messages.success(req,
                             "Campaign Created Successfully!")
            return HttpResponseRedirect("/home")
    else:
        projectForm = ProjectForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    context['form'] = projectForm
    context['formset'] = formset
    return render(req, "projects/create.html", context)
