from django.urls import path, include
from authenticate import views
from django.contrib.auth.views import LoginView 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', LoginView.as_view(template_name='authenticate/login.html') ),
    path('social-auth/', include('social_django.urls', namespace="social")),
    #path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
