from django.urls import path
from authenticate import views
urlpatterns = [
    path('login', views.login)
]
