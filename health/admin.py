from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AmbulanceRequest, HealthCamp, DoctorAppointment

@admin.register(AmbulanceRequest)
class AmbulanceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'emergency_type', 'location', 'status')
    list_filter = ('status', 'emergency_type')
    search_fields = ('user__username', 'location')

@admin.register(HealthCamp)
class HealthCampAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'doctors_available', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('location',)

@admin.register(DoctorAppointment)
class DoctorAppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'camp', 'preferred_time', 'status')
    list_filter = ('status', 'camp')
    search_fields = ('user__username',)