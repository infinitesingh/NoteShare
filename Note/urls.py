# notes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('notes/', views.note_list, name='note_list'),

    path('notes/add/', views.note_create, name='note_create'),
    path('notes/edit/<int:note_id>/', views.note_edit, name='note_edit'),
    path('notes/delete/<int:note_id>/', views.note_delete, name='note_delete'),
    path('notes/share/<int:note_id>/', views.note_share, name='note_share'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),

]
