from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_started, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Public registration for new users
    path('register/', views.register, name='register'),

    # Admin-only registration (keep your old view)
    path('register-user/', views.register_user, name='register_user'),
]
