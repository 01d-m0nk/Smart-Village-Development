from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_grievance, name='create_grievance'),
    path('my/', views.my_grievances, name='my_grievances'),
    path('<int:pk>/', views.grievance_detail, name='grievance_detail'),

    path('all/', views.all_grievances, name='all_grievances'),
    path('<int:pk>/update/', views.update_grievance, name='update_grievance'),
]