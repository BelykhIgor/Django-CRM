"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import handler403
from django.shortcuts import render


urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls')),
    path('customers/', include('customers.urls')),
    path('contracts/', include('contracts.urls')),
    path('ads/', include('ads.urls')),
    path('products/', include('products.urls')),
    path('users/', include('user_auth.urls')),
    path('accounts/', include('user_auth.urls')),
    path('', include('client_stat.urls')),
]

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls"))
    )

def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

handler403 = custom_permission_denied_view
