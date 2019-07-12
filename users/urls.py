from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #
    #path('login/', views.user_login, name='login'),
    #path('login/',auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    #path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('register/',views.register, name='register'),
    #path('login/',views.login, name='login'),
    #path('logout/', views.user_logout, name='logout'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
