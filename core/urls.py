from django.urls import path
from . import views

urlpatterns = [
    path('v/', views.tryy, name='try'),
    path('create/', views.create_activity, name='create_activity'),
    path('update/<int:activity_id>/', views.update_activity, name='update_activity'),
    path('', views.activity_list, name='activity_list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_registration, name='registration'),
    path('activity/<int:activity_id>/delete/', views.delete_activity, name='delete_activity'),
    path('activity/updates/', views.activity_updates_per_day, name='activity_updates_per_day'),
    path('activity/history/', views.activity_history_report, name='activity_history_report'),
    path('activity/<int:activity_id>/history/', views.activity_history, name='activity_history'),
    path('activity/<int:activity_id>/delete_history/', views.delete_activity_history, name='delete_activity_history'),
]

