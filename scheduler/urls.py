from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/<int:pk>/delete/', views.delete_appointment, name='delete_appointment'),
    path('appointments/<int:pk>/edit/', views.edit_appointment, name='edit_appointment'),
    path('clients/', views.clients, name='clients'),
    path('clients/<int:pk>/delete/', views.delete_client, name='delete_client'),
    path('students/', views.students, name='students'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('setup/', views.setup, name='setup'),
]