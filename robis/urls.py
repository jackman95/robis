"""
URL configuration for robis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from personal.views import (
    home_screen_view,
    version_view,
    napoveda_view,
)

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
    account_event_view,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),
    path('registrace/', registration_view, name="register"),
    path('odhlaseni/', logout_view, name="logout"),
    path('prihlaseni/', login_view, name="login"),
    path('ucet/', account_view, name="account"),
    path('ucet_zavody/', account_event_view, name="account_event"),
    path('pristup/', must_authenticate_view, name="must_authenticate"),
    path('kalendar/', include('kalendar.urls', "kalendar")),
    path('verze/', version_view, name="version"),
    path('napoveda/', napoveda_view, name="napoveda"),
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('zmena_hesla/dokonceno/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('zmena_hesla/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('reset_hesla/dokonceno/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_hesla/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/dokonceno/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)