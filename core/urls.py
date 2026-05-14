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
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path(
        'project/<int:project_id>/',
        project_detail,
        name='project_detail'
    ),
    path('resource/<int:resource_id>/summary/', generate_resource_summary, name='generate_resource_summary'),
    path(
    'summary/delete/<int:summary_id>/',
    views.delete_summary,
    name='delete_summary'),
    path(
    'resource/delete/<int:resource_id>/',
    views.delete_resource,
    name='delete_resource'
    ),
    path(
    'project/<int:project_id>/export/pdf/',
    views.export_project_pdf,
    name='export_project_pdf'),
]