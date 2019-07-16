from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('clients/', views.client, name='client_base'),
    path('client_info_list/', views.client_info_list, name='client_info_list'),
    path('add_client/', views.add_client, name='add_client'),
    path('addClientToDatabase/', views.addClientToDatabase, name='addClientToDatabase'),


]
