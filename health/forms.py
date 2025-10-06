from django import forms
from .models import AmbulanceRequest, DoctorAppointment, HealthCamp

class AmbulanceRequestForm(forms.ModelForm):
    class Meta:
        model = AmbulanceRequest
        fields = ['emergency_type', 'location']

class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = DoctorAppointment
        fields = ['camp', 'preferred_time']

class HealthCampForm(forms.ModelForm):
    class Meta:
        model = HealthCamp
        fields = ['date', 'location', 'description', 'doctors_available', 'is_active']