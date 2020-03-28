from django.urls import path, include
from authenticate import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login', LoginView.as_view(template_name='authenticate/login.html'), name='auth.login'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    # path('login', views.login_user),
    # path('logout', views.logout_user, name='auth.logout'),
    path('register/', views.register, name='register'),

]


# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']