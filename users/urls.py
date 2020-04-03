from django.urls import path, include
from users import views

urlpatterns = [
    path('profile', views.profile, name="profile"),
    path('delete_profile', views.delete_profile, name="delete_profile")
]
