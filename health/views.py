from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AmbulanceRequest, HealthCamp, DoctorAppointment
from .forms import AmbulanceRequestForm, DoctorAppointmentForm, HealthCampForm

@login_required
def request_ambulance(request):
    if request.method == 'POST':
        form = AmbulanceRequestForm(request.POST)
        if form.is_valid():
            ambulance = form.save(commit=False)
            ambulance.user = request.user
            ambulance.save()
            return redirect('dashboard')
    else:
        form = AmbulanceRequestForm()
    
    return render(request, 'health/ambulance_request.html', {'form': form})

@login_required
def book_appointment(request):
    active_camps = HealthCamp.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = DoctorAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('dashboard')
    else:
        form = DoctorAppointmentForm()
    
    return render(request, 'health/book_appointment.html', {
        'form': form,
        'active_camps': active_camps
    })

@login_required
def health_dashboard(request):
    context = {
        'ambulance_requests': AmbulanceRequest.objects.filter(user=request.user),
        'appointments': DoctorAppointment.objects.filter(user=request.user),
        'active_camps': HealthCamp.objects.filter(is_active=True)
    }
    return render(request, 'health/dashboard.html', context)

# Admin Views
@login_required
def manage_camps(request):
    if not request.user.is_superuser:
        return redirect('health_dashboard')
    
    if request.method == 'POST':
        form = HealthCampForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_camps')
    else:
        form = HealthCampForm()
    
    return render(request, 'health/manage_camps.html', {
        'form': form,
        'camps': HealthCamp.objects.all()
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import AmbulanceRequest, HealthCamp, DoctorAppointment
from .forms import HealthCampForm

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def manage_camps(request):
    if request.method == 'POST':
        form = HealthCampForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('health:manage_camps')
    else:
        form = HealthCampForm()

    context = {
        'form': form,
        'camps': HealthCamp.objects.all().order_by('-date'),
        'ambulance_requests': AmbulanceRequest.objects.all().order_by('-timestamp'),
        'appointments': DoctorAppointment.objects.all().order_by('-timestamp')
    }
    return render(request, 'health/manage_camps.html', context)

@login_required
@user_passes_test(is_admin)
def edit_camp(request, camp_id):
    camp = get_object_or_404(HealthCamp, id=camp_id)
    if request.method == 'POST':
        form = HealthCampForm(request.POST, instance=camp)
        if form.is_valid():
            form.save()
            return redirect('health:manage_camps')
    else:
        form = HealthCampForm(instance=camp)
    
    return render(request, 'health/edit_camp.html', {
        'form': form,
        'camp': camp
    })

@login_required
@user_passes_test(is_admin)
def update_request(request, request_id, status):
    ambulance_request = get_object_or_404(AmbulanceRequest, id=request_id)
    ambulance_request.status = status
    ambulance_request.save()
    return redirect('health:manage_camps')

@login_required
@user_passes_test(is_admin)
def update_appointment(request, appointment_id, status):
    appointment = get_object_or_404(DoctorAppointment, id=appointment_id)
    appointment.status = status
    appointment.save()
    return redirect('health:manage_camps')