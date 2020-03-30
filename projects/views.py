from django.shortcuts import render, get_object_or_404, redirect
from projects.forms import ProjectForm, ImageForm, CommentForm
from django.http import HttpResponse
from django.forms import modelformset_factory
from projects.models import Image, Project, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum
from decimal import Decimal
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.

def index(req):
    context = {}
    projects = Project.objects.all()
    context['projects'] = projects
    return render(req, "projects/index.html", context)


def show(req, project_slug):
    context = {}
    project = get_object_or_404(Project, slug=project_slug)
    comments = project.comments.filter(parent__active__isnull=True)
    similar_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project.id)
    comment_form = CommentForm()
    context['project'] = project
    context['similar_projects'] = similar_projects
    context['comments'] = comments
    context['comment_form'] = comment_form
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


@login_required
def add_donations(req):
    if req.POST:
        project_slug = req.POST.get("project")
        amount = req.POST.get("amount")
        project = Project.objects.get(slug=project_slug)
        all_donations = project.donations.aggregate(Sum('amount'))
        # return HttpResponse(all_donations['amount__sum'])
        valid_amount = project.total - (all_donations['amount__sum'] + Decimal(amount))
        if project.owner != req.user and valid_amount >= 0:
            project.donations.create(amount=amount)
            messages.success(req, "Donation added successfully")
        else:
            messages.error(req, "Sorry, donation failed please try again later!!")
        return redirect("projects.show", project_slug=project_slug)
    return HttpResponseRedirect(req.META.get('HTTP_REFERER', '/'))


@login_required
def add_comment(req, project_slug):
    data = {}
    if req.method == 'POST':
        project = Project.objects.get(slug=project_slug)
        comment_form = CommentForm(data=req.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            parent = req.POST.get('parent')
            if parent:
                parent_comment = Comment.objects.get(id=parent)
                new_comment.parent = parent_comment
            new_comment.project = project
            new_comment.user = req.user
            new_comment.save()
            comments = project.comments.filter(parent__active__isnull=True)
            data['status'] = True
            data['html'] = render_to_string("projects/_comments.html", {'comments': comments, 'project': project}, req)
    else:
        data['error_message'] = 'Error, please try again later'

    return JsonResponse(data)
