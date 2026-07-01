from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.students_list, name='students_list'),
    path('add/', views.students_add, name='students_add'),
    path('edit/<int:pk>/', views.students_edit, name='students_edit'),
    path('delete/<int:pk>/', views.students_delete, name='students_delete'),
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
]