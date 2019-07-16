from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('projects/', views.project, name='project_base'),
    path('projects_list/', views.project_info_list, name='project_info_list'),
    path('add_project/', views.add_project, name='add_project'),
    path('addProjectToDatabase/', views.addProjectToDatabase, name='addProjectToDatabase'),

]
