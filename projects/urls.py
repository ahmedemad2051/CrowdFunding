from django.urls import path, include
from projects import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name="projects.all"),
    path('show/<slug:project_slug>', views.show, name="projects.show"),
    path('create', views.create, name="projects.create"),
    path('edit/<slug:project_slug>', views.update, name="projects.update"),
    path('add_donations', views.add_donations, name="projects.add_donations"),
    path('add_reports', views.add_reports, name="projects.add_reports"),
    path('add_comment/<slug:project_slug>', views.add_comment, name="projects.add_comment"),
    path('cancel/<slug:project_slug>', views.cancel_project, name="projects.cancel"),
    path('ratings', include('star_ratings.urls', namespace='ratings')),
]
