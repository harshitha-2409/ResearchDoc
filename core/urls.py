from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    home,
    register_view,
    dashboard,
    project_detail
)
from .views import home, register_view, dashboard, project_detail, generate_resource_summary


urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(template_name='core/login.html'),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),

    path('dashboard/', views.dashboard, name='dashboard'),

    path(
        'project/<int:project_id>/',
        views.project_detail,
        name='project_detail'
    ),

    path(
        'project/<int:project_id>/edit/',
        views.edit_project,
        name='edit_project'
    ),

    path(
    'project/<int:project_id>/delete/',
    views.delete_project,
    name='delete_project'
    ),

    path(
        'project/<int:project_id>/export/pdf/',
        views.export_project_pdf,
        name='export_project_pdf'
    ),

    path(
        'resource/<int:resource_id>/summary/',
        views.generate_resource_summary,
        name='generate_resource_summary'
    ),

    path(
        'resource/delete/<int:resource_id>/',
        views.delete_resource,
        name='delete_resource'
    ),

    path(
        'summary/delete/<int:summary_id>/',
        views.delete_summary,
        name='delete_summary'
    ),

    path(
        'resource/<int:resource_id>/edit/',
        views.edit_resource,
        name='edit_resource'
    ),

    path(
        'comparison/<int:comparison_id>/edit/',
        views.edit_comparison,
        name='edit_comparison'
    ),

    path(
        'comparison/<int:comparison_id>/delete/',
        views.delete_comparison,
        name='delete_comparison'
    ),

    path(
        'summary/<int:summary_id>/edit/',
        views.edit_summary,
        name='edit_summary'
    ),
    path(
        'project/<int:project_id>/restore/',
        views.restore_project,
        name='restore_project'
    ),
]