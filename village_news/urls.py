from django.urls import path
from . import views

app_name = 'village_news'

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('category/<str:category>/', views.announcement_category, name='announcement_category'),
    path('detail/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('create/', views.announcement_create, name='announcement_create'),
    path('alerts/', views.user_alerts, name='user_alerts'),
    path('alert/read/<int:pk>/', views.mark_alert_read, name='mark_alert_read'),
]