from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class AmbulanceRequest(models.Model):
    EMERGENCY_TYPES = [
        ('ACC', 'Accident'),
        ('HRT', 'Heart Attack'),
        ('DEL', 'Delivery'),
        ('OTH', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emergency_type = models.CharField(max_length=3, choices=EMERGENCY_TYPES)
    location = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending', 
              choices=[('Pending', 'Pending'), ('Dispatched', 'Dispatched'), ('Completed', 'Completed')])

class HealthCamp(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    doctors_available = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

class DoctorAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    camp = models.ForeignKey(HealthCamp, on_delete=models.CASCADE)
    preferred_time = models.TimeField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Booked', 
              choices=[('Booked', 'Booked'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])