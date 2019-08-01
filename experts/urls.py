from django.urls import path
from . import views as experts_views
from django.contrib.auth import views as auth_views
from . import views_update as update_views

urlpatterns = [
    path('', experts_views.base, name='base'),
    path('addexpert/', experts_views.addExpert, name='addexpert'),
    path('home/', experts_views.base, name='home'),


    path('addcomment/<int:eid>/<str:ename>/', experts_views.add_comment, name='add_comment'),
    path('addworkexp/<int:eid>/<str:ename>/', experts_views.add_workexp, name='add_workexp'),

    path('addcomplete/', experts_views.addok, name='addcomplete'),


    path('updateexpert/', update_views.expertInfoUpdate, name='updateexpert'),
    path('expertinfolist/', experts_views.expertInfo_list, name='expertinfolist'),
    path('<str:ename>/<int:eid>/', experts_views.expert_detail, name='expert_detail'),
    path('update/<str:ename>/<int:eid>/', experts_views.expert_detail_update, name='expert_detail_update'),
    path('contact_info_update/<str:ename>/<int:eid>/', experts_views.expert_contact_info_update, name='expert_contact_info_update'),
    path('expertinfoupdatetodatabase/', update_views.expertInfoUpdateToDatabase, name='expertinfoupdatetodatabase'),

    path('<int:eid>/<str:ename>/commentdetail/', experts_views.comment_detail, name='comment_detail'),
    path('update/<int:eid>/<int:cmtid>/commentdetail/', experts_views.comment_detail_update, name='comment_detail_update'),

    path('<int:eid>/<str:ename>/workexpdetail/', experts_views.workexp_detail, name='workexp_detail'),
    path('update/<int:eid>/<int:expid>/workexpdetail/', experts_views.workexp_detail_update, name='workexp_detail_update'),

    path('deleteexpert/', update_views.expertInfoDelete, name='deleteexpert'),
    path('delete_confirm/<int:eid>/<str:ename>/', experts_views.delete_confirm, name='delete_confirm'),
    path('delete/<int:eid>/<str:ename>/', experts_views.myDelete, name='myDelete'),
    path('expertinfodeletefromdatabase/', update_views.expertInfoDeleteFromDatabase, name='expertinfodeletefromdatabase'),

    path('deletecomment/<int:eid>/<int:cmtid>/', update_views.delete_comment, name='delete_comment'),
    path('deleteworkexp/<int:eid>/<int:expid>/', update_views.delete_workexp, name='delete_workexp'),
    path('deleteworkexpconfirm/<int:eid>/<int:expid>/', update_views.delete_workexp_confirm, name='delete_workexp_confirm'),
    path('deletecommentconfirm/<int:eid>/<int:cmtid>/', update_views.delete_comment_confirm, name='delete_comment_confirm'),

    path('search_expert/', experts_views.search_expert, name='search_expert'),
    path('advanced_expert_search/', experts_views.advanced_expert_search, name='advanced_expert_search'),
    path('advanced_expert/', experts_views.advanced_expert_form, name='advanced_expert_form'),

    path('expert_payment/<int:ep_id>/edit', experts_views.get_payment_update, name='get_payment_update'),


]
