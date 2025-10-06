from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Opportunity, Application, OpportunityCategory
from .forms import OpportunityForm, ApplicationForm

@login_required
def post_opportunity(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can post opportunities")
        return redirect('opportunities_list')
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.posted_by = request.user
            opportunity.save()
            messages.success(request, "Opportunity posted successfully!")
            return redirect('opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm()
    
    return render(request, 'opportunities/post_opportunity.html', {'form': form})

def opportunity_list(request):
    opportunities = Opportunity.objects.filter(is_active=True).order_by('-posted_at')
    return render(request, 'opportunities/opportunity_list.html', {'opportunities': opportunities})

def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        application_form = ApplicationForm(request.POST, request.FILES)
        if application_form.is_valid():
            application = application_form.save(commit=False)
            application.opportunity = opportunity
            application.applicant = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('opportunity_detail', pk=opportunity.pk)
    else:
        application_form = ApplicationForm()
    
    return render(request, 'opportunities/opportunity_detail.html', {
        'opportunity': opportunity,
        'form': application_form
    })

@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'opportunities/my_applications.html', {'applications': applications})

@login_required
def all_applications(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can view all applications")
        return redirect('opportunities_list')
    
    applications = Application.objects.all().order_by('-applied_at')
    return render(request, 'opportunities/all_applications.html', {
        'applications': applications
    })

@login_required
def manage_applications(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can manage applications")
        return redirect('opportunities_list')
    
    opportunity = get_object_or_404(Opportunity, pk=pk)
    applications = opportunity.applications.all().order_by('status', 'applied_at')
    return render(request, 'opportunities/manage_applications.html', {
        'opportunity': opportunity,
        'applications': applications
    })
@login_required
def update_application_status(request, pk, status):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can update application status")
        return redirect('opportunities_list')
    
    application = get_object_or_404(Application, pk=pk)
    application.status = status
    application.save()
    messages.success(request, f"Application status updated to {status}")
    return redirect('manage_applications', pk=application.opportunity.pk)