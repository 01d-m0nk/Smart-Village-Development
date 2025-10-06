from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Announcement, UserAlert
from .forms import AnnouncementForm
from django.shortcuts import render

def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    paginator = Paginator(announcements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get category choices for sidebar
    category_choices = Announcement.CATEGORY_CHOICES
    
    return render(request, 'village_news/list.html', {
        'page_obj': page_obj,
        'announcement_categories': category_choices
    })

def announcement_category(request, category):
    announcements = Announcement.objects.filter(category=category).order_by('-created_at')
    category_name = dict(Announcement.CATEGORY_CHOICES).get(category, 'Announcements')
    category_choices = Announcement.CATEGORY_CHOICES
    
    return render(request, 'village_news/category.html', {
        'announcements': announcements,
        'category': category_name,
        'announcement_categories': category_choices
    })

def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    category_choices = Announcement.CATEGORY_CHOICES
    
    # Mark alert as read if user is viewing the announcement
    if request.user.is_authenticated:
        UserAlert.objects.filter(
            user=request.user, 
            announcement=announcement,
            is_read=False
        ).update(is_read=True)
    
    return render(request, 'village_news/detail.html', {
        'announcement': announcement,
        'announcement_categories': category_choices
    })

@login_required
def announcement_create(request):
    if not request.user.is_superuser:
        messages.error(request, "Only administrators can create announcements.")
        return redirect('village_news:announcement_list')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.posted_by = request.user
            announcement.save()
            messages.success(request, "Announcement created successfully!")
            return redirect('village_news:announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm(user=request.user)
    
    category_choices = Announcement.CATEGORY_CHOICES
    return render(request, 'village_news/create.html', {
        'form': form,
        'announcement_categories': category_choices
    })

@login_required
def user_alerts(request):
    alerts = UserAlert.objects.filter(user=request.user).order_by('-created_at')
    category_choices = Announcement.CATEGORY_CHOICES
    
    return render(request, 'village_news/alerts.html', {
        'alerts': alerts,
        'announcement_categories': category_choices
    })

@login_required
def mark_alert_read(request, pk):
    alert = get_object_or_404(UserAlert, pk=pk, user=request.user)
    alert.is_read = True
    alert.save()
    return redirect('village_news:announcement_detail', pk=alert.announcement.pk)
