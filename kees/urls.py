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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

import core.views
from ariadne.contrib.django.views import GraphQLView
from core.schema import schema

urlpatterns = [
    path('', core.views.startpage, name='startpage'),
    path('dashboard/', core.views.dashboard, name='dashboard'),
    path('cases/', core.views.case_list, name='cases'),
    path('cases/create/<int:case_type_id>/',
         core.views.create_case, name='create_case'),
    path('cases/view/<int:case_id>/', core.views.view_case, name='view_case'),
    path('cases/view/<int:case_id>/phase/<int:phase_id>',
         core.views.view_case, name='view_case_phase'),
    path('cases/view/<int:case_id>/claim',
         core.views.claim_case, name='claim_case'),
    path('cases/view/<int:case_id>/change_assignee',
         core.views.change_assignee, name='change_assignee'),
    path('cases/view/<int:case_id>/change_phase',
         core.views.change_phase, name='change_phase'),
    path('cases/view/<int:case_id>/next_phase',
         core.views.next_phase, name='next_phase'),
    path('cases/delete/<int:case_id>/',
         core.views.delete_case, name='delete_case'),
    path('cases/view/<int:case_id>/attachments',
         core.views.attachments, name='attachments'),
    path('cases/view/<int:case_id>/attachments/create/',
         core.views.create_attachment, name='create_attachment'),
    path('cases/view/<int:case_id>/attachments/delete/<int:attachment_id>/',
         core.views.delete_attachment, name='delete_attachment'),
    path('cases/view/<int:case_id>/logs', core.views.logs, name='logs'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('graphql', GraphQLView.as_view(schema=schema), name='graphql'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
