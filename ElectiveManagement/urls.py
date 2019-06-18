"""ElectiveManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

admin.site.site_header = 'NITH Elective Administration'
admin.site.site_title = 'NITH Elective Course Management System'
admin.site.index_title = 'Elective Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='User/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='User/logout.html'), name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='User/password-reset.html'), name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(template_name='User/password-reset-done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='User/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='User/password-reset-complete.html'), name='password_reset_complete'),
    path('', include('Elective.urls')),
    path('', include('Subject.urls')),
    path('', include('Application.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)