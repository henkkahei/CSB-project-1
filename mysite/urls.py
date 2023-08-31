"""
URL configuration for mysite project.

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
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

from . import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("polls/", include("polls.urls")),
        path('login/', LoginView.as_view(template_name='registration/login.html')),
    	path('logout/', LogoutView.as_view(), name='logout'),
        path('admin/', admin.site.urls),
        path("accounts/", include("django.contrib.auth.urls")),
        path("__debug__/", include("debug_toolbar.urls")),
        path('', TemplateView.as_view(template_name='home.html'), name='home'),
    ]
