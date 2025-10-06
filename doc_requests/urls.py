from django.urls import path
from . import views

app_name = 'doc_requests'

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('my-requests/', views.user_requests, name='user_requests'),
    path('submit/<int:request_id>/', views.submit_document, name='submit_document'),
]