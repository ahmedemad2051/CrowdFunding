from django.urls import path, include
from django.conf.urls import url
from allauth.account.views import ConfirmEmailView
from . import views


urlpatterns = [
    url(r'^registration/account-email-verification-sent/', views.null_view, name='account_email_verification_sent'),
    url(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(r'^registration/complete/$', views.complete_view, name='account_confirm_complete'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.null_view, name='password_reset_confirm'),
    url(r'', include('rest_auth.urls')),
    url(r'^registration/', include('rest_auth.registration.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('register/', views.register, name='register'),
]
