"""kees URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path

import core.views

urlpatterns = [
    path('', core.views.startpage, name='startpage'),
    path('dashboard/', core.views.dashboard, name='dashboard'),
    path('overview/', core.views.overview, name='overview'),
    path('cases/create/<int:case_type_id>/', core.views.create_case, name='create_case'),
    path('cases/view/<int:case_id>/', core.views.view_case, name='view_case'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
