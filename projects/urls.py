from django.urls import path
from projects import views
urlpatterns = [
    path('',views.index, name="projects.all"),
    path('show/<slug:project_slug>',views.show, name="projects.show"),
    path('create',views.create, name="projects.create"),
    path('add_donations',views.add_donations, name="projects.add_donations"),
]
