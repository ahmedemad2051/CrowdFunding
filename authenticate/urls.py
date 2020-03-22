from django.urls import path
from authenticate import views
from django.contrib.auth.views import LoginView 

urlpatterns = [
    path('login', LoginView.as_view(template_name='authenticate/login.html') ),

]
