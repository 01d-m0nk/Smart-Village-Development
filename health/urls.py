from django.urls import path
from . import views

app_name = 'health'

urlpatterns = [
    path('', views.health_dashboard, name='health_dashboard'),
    path('request-ambulance/', views.request_ambulance, name='request_ambulance'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('manage-camps/', views.manage_camps, name='manage_camps'),
    path('manage-camps/', views.manage_camps, name='manage_camps'),
    path('edit-camp/<int:camp_id>/', views.edit_camp, name='edit_camp'),
    path('update-request/<int:request_id>/<str:status>/', views.update_request, name='update_request'),
    path('update-appointment/<int:appointment_id>/<str:status>/', views.update_appointment, name='update_appointment'),
]