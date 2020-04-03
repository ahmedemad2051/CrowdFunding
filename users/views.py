from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Image, Project, Comment, Donation
from users.models import Account

# Create your views here.
@login_required
def profile(request):
    context = {}

    user_projects = Project.objects.filter(owner=request.user)  # get user projects
    donations = Project.objects.filter(donations__user=request.user)  # get user projects

    user_obj = Account.objects.get(email=request.user)

    email = getattr(user_obj, 'email')
    username = getattr(user_obj, 'username')
    first_name = getattr(user_obj, 'first_name')
    last_name = getattr(user_obj, 'last_name')
    mobile = getattr(user_obj, 'mobile')
    profile_picture = getattr(user_obj, 'profile_picture')
    facebook = getattr(user_obj, 'facebook')
    instagram = getattr(user_obj, 'instagram')
    twitter = getattr(user_obj, 'twitter')
    public_info = getattr(user_obj, 'public_info')

    context['user_projects'] = user_projects
    context['donations'] = donations

    context['email'] = email
    context['username'] = username
    context['first_name'] = first_name
    context['last_name'] = last_name
    context['mobile'] = mobile
    context['profile_picture'] = profile_picture
    context['facebook'] = facebook
    context['instagram'] = instagram
    context['twitter'] = twitter
    context['public_info'] = public_info

    return render(request, "users/profile.html", context)

