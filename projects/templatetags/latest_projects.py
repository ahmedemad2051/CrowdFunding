from django import template

from projects.models import Project

register = template.Library()


@register.filter(name='latest_projects')
@register.simple_tag
def latest_projects():
    last_two_projects = Project.objects.filter(enable=True).order_by('-created_at')[:2]
    return last_two_projects

