from django.shortcuts import render, get_object_or_404, redirect
from projects.forms import ProjectForm, ImageForm, CommentForm
from django.http import HttpResponse
from django.forms import modelformset_factory
from projects.models import Image, Project, Comment, Report
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
    projects = Project.objects.filter(enable=True)
    if 'category' in req.GET:
        category = req.GET.get('category')
        context['category'] = category
        projects = projects.filter(category__name=category)

    context['projects'] = projects
    return render(req, "projects/index.html", context)


def show(req, project_slug):
    context = {}
    project = get_object_or_404(Project, slug=project_slug)
    if not project.enable and project.owner != req.user:
        return redirect("projects.all")
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
def update(req, project_slug):
    context = {}
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)
    project = get_object_or_404(Project, slug=project_slug, owner=req.user)
    project_form = ProjectForm(req.POST or None, instance=project)
    if req.method == "POST":
        formset = ImageFormSet(req.POST, req.FILES,
                               queryset=project.images.all())
        if project_form.is_valid() and formset.is_valid():
            project = project_form.save(commit=False)
            project.owner = req.user
            project.save()
            project_form.save_m2m()

            for form in formset.cleaned_data:
                if 'image' in form:
                    image = form['image']
                    photo = Image(project=project, image=image)
                    photo.save()

            messages.success(req, "Campaign Updated Successfully!")
            return redirect("projects.show", project_slug)
    else:
        formset = ImageFormSet(queryset=project.images.all())
    context['project'] = project
    context['form'] = project_form
    context['formset'] = formset
    return render(req, "projects/update.html", context)


def get_project_donations(project):
    all_donations = project.donations.aggregate(Sum('amount'))
    # return HttpResponse(all_donations['amount__sum'])
    amount__sum = all_donations['amount__sum']
    if not amount__sum:
        amount__sum = 0
    return amount__sum


@login_required
def add_donations(req):
    if req.POST:
        project_slug = req.POST.get("project")
        amount = req.POST.get("amount")
        project = Project.objects.get(slug=project_slug)
        amount__sum = get_project_donations(project)
        valid_amount = project.total - (amount__sum + Decimal(amount))
        if project.owner != req.user and valid_amount >= 0 and project.enable:
            project.donations.create(amount=amount, user=req.user)
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


@login_required
def add_reports(req):
    if req.POST:
        report_type = req.POST.get('report_type')
        report_for = req.POST.get('report_for')
        content = req.POST.get('content')
        if report_type == 'project':
            obj = get_object_or_404(Project, id=report_for)
        else:
            obj = get_object_or_404(Comment, id=report_for)
        report = Report(user=req.user, content=content)
        report.report_for = obj
        report.save()
        messages.success(req, "Report Added Successfully")
    return HttpResponseRedirect(req.META.get('HTTP_REFERER', '/'))


@login_required
def cancel_project(req, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    amount__sum = get_project_donations(project)
    donations_percent = int((amount__sum * 100) / project.total)
    if project.owner == req.user and donations_percent < 25:
        project.enable = False
        project.save()
        messages.success(req, f'project {project.title} has been cancelled!!')
    else:
        messages.error(req,
                       "Sorry,You can not cancel the project either you don't have right permissions or project donations up to 25%")
    return redirect("projects.show", project_slug=project_slug)
