from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunities_list'),
    path('post/', views.post_opportunity, name='post_opportunity'),
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('<int:pk>/apply/', views.opportunity_detail, name='apply_opportunity'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('applications/manage/', views.all_applications, name='all_applications'),  # New view for all applications
    path('<int:pk>/manage/', views.manage_applications, name='manage_applications'),
    path('applications/<int:pk>/<str:status>/', views.update_application_status, name='update_application'),
]