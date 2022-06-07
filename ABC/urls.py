"""ABC URL Configuration

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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.static import serve
from AbcApp import views

admin.site.site_header = "ABC NextGen Dashboard"
admin.site.site_title = "ABC NextGen Admin Dashboard"
admin.site.index_title = "Welcome to ABC NextGen Admin Dashboard"

urlpatterns = [
                  path('', views.root, name='root'),
                  path('bulk/',views.create_bulk_zip, name="bulk"),
                  path('dashboard/', views.root, name='dashboard'),
                  path('download/', views.export_to_csv, name='download_summary'),
                  path('admin/', admin.site.urls),
                  path('oauth2/', include('django_auth_adfs.urls')),
                  url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                  url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
              ]
