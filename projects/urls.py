from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('projects/', views.project, name='project_base'),
    path('project_info_list/', views.project_info_list, name='project_info_list'),
    path('add_project/', views.add_project, name='add_project'),
    path('addProjectToDatabase/', views.addProjectToDatabase, name='addProjectToDatabase'),
    path('project_detail/<int:pid>/<int:cid>/', views.project_detail, name='project_detail'),
    path('projects/add_p2e/<int:pid>/', views.add_p2e, name='add_p2e'),
    path('projects/update_p2e_detail/<int:pteid>/', views.update_p2e_detail, name='update_p2e_detail'),
    path('projects/update/<int:pid>/', views.update_project_detail, name='update_project_detail'),

    path('projects/delete_project/<int:pid>/', views.delete_project, name='delete_project'),
    path('projects/delete_p2e/<int:pteid>/<int:pid>', views.delete_p2e, name='delete_p2e'),

    path('projects/advanced_project_search/', views.advanced_project_search, name='advanced_project_search'),
    path('projects/advanced_project/', views.advanced_project_form, name='advanced_project_form'),

]
#     path('projects/update_pm_contact_info/<int:pid>', views.pm_contact_info_update, name='pm_contact_info_update'),