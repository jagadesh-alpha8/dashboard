from django.contrib import admin
from django.urls import path, include
from lookerapp import views
from django.conf.urls import handler404
from django.contrib.auth import views as auth_views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.views.generic import RedirectView


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('admin/', admin.site.urls),
    path('accounts/login/', views.login_view, name='login'),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('edutech/', views.edutech, name='edutech'),
    path('edu/', views.edu, name='edu'),
    path('trainer/', views.trainer, name='trainer'),
    path('filter/', views.filter_photos, name='filter_photos'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

handler404 = 'lookerapp.views.handler404'