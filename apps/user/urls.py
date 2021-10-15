from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.user, name = 'user'),
    path('loginPage', views.loginPage, name = 'loginPage'),
    path('register', views.register, name = 'register'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('modify_user', views.modify_user, name='modify_user'),
    path('modify_pass', views.modify_pass, name='modify_pass'),
    path('logoutUSer', views.logoutUser, name= 'logoutUser'),

    path('reset_password', auth_views.PasswordResetView.as_view(template_name='user/pass_reset.html'), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='user/pass_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='user/pass_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='user/pass_reset_complete.html'), name='password_reset_complete'),
]
