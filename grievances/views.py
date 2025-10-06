from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Grievance, IssueCategory
from .forms import GrievanceForm, GrievanceAdminForm
from accounts.models import CustomUser
from django.utils import timezone

@login_required
def create_grievance(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST, request.FILES)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.user = request.user
            grievance.save()
            messages.success(request, 'Grievance submitted successfully!')
            return redirect('my_grievances')
    else:
        form = GrievanceForm()
    
    # Debug output (check your server console)
    print("Categories in database:", IssueCategory.objects.all())
    print("Form category choices:", form.fields['category'].queryset)
    
    return render(request, 'grievances/create.html', {'form': form})

@login_required
def my_grievances(request):
    grievances = Grievance.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'grievances/my_grievances.html', {'grievances': grievances})

@login_required
def grievance_detail(request, pk):
    grievance = get_object_or_404(Grievance, pk=pk)
    if not (request.user == grievance.user or request.user.is_superuser):
        messages.error(request, 'You are not authorized to view this grievance')
        return redirect('dashboard')
    
    return render(request, 'grievances/detail.html', {'grievance': grievance})

@login_required
def all_grievances(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('dashboard')
    
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    
    grievances = Grievance.objects.all().order_by('-created_at')
    
    if status_filter:
        grievances = grievances.filter(status=status_filter)
    if category_filter:
        grievances = grievances.filter(category_id=category_filter)
    
    categories = IssueCategory.objects.all()
    return render(request, 'grievances/all_grievances.html', {
        'grievances': grievances,
        'categories': categories,
        'status_choices': Grievance.STATUS_CHOICES,
        'selected_status': status_filter,
        'selected_category': category_filter,
    })

@login_required
def update_grievance(request, pk):
    grievance = get_object_or_404(Grievance, pk=pk)
    
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to update this grievance')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = GrievanceAdminForm(request.POST, request.FILES, instance=grievance)
        if form.is_valid():
            updated_grievance = form.save(commit=False)
            
            # Remove or modify this line if you're not using resolved_at
            if updated_grievance.status == 'RESOLVED':
                # Just save without checking resolved_at
                pass
                
            updated_grievance.save()
            messages.success(request, 'Grievance updated successfully!')
            return redirect('all_grievances')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = GrievanceAdminForm(instance=grievance)
    
    return render(request, 'grievances/update.html', {
        'form': form,
        'grievance': grievance
    })