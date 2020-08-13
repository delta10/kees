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
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework import routers

from core import viewsets, views

router = routers.DefaultRouter()
router.register(r'cases', viewsets.CaseViewSet)
router.register(r'attachments', viewsets.AttachmentViewSet)

admin.site.site_header = 'Kees beheer'
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('', views.startpage, name='startpage'),
    path('api/', include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cases/', views.case_list, name='cases'),
    path('cases/create/<int:case_type_id>/',
         views.create_case, name='create_case'),
    path('cases/view/<int:case_id>/', views.view_case, name='view_case'),
    path('cases/view/<int:case_id>/phase/<int:phase_id>',
         views.view_case, name='view_case_phase'),
    path('cases/view/<int:case_id>/claim',
         views.claim_case, name='claim_case'),
    path('cases/view/<int:case_id>/change_assignee',
         views.change_assignee, name='change_assignee'),
    path('cases/view/<int:case_id>/change_phase',
         views.change_phase, name='change_phase'),
    path('cases/view/<int:case_id>/next_phase',
         views.next_phase, name='next_phase'),
    path('cases/delete/<int:case_id>/',
         views.delete_case, name='delete_case'),
    path('cases/view/<int:case_id>/attachments',
         views.attachments, name='attachments'),
    path('cases/view/<int:case_id>/attachments/create/<str:attachment_type>/',
         views.create_attachment, name='create_attachment'),
    path('cases/view/<int:case_id>/attachments/delete/<int:attachment_id>/',
         views.delete_attachment, name='delete_attachment'),
    path('cases/view/<int:case_id>/logs', views.logs, name='logs'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
