from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator  # Add this import
import os

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'grievances':
        default_categories = [
            ("Water Supply", "Issues related to water infrastructure"),
            ("Street Lights", "Problems with public lighting"),
            ("Road Maintenance", "Road and pavement repairs"),
            ("Waste Management", "Garbage collection issues"),
        ]
        
        for name, description in default_categories:
            IssueCategory.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )

class IssueCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

def grievance_image_path(instance, filename):
    """Generate path for uploaded images"""
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join(
        'grievances',
        str(instance.user.id),
        timezone.now().strftime('%Y/%m'),
        filename
    )

class Grievance(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grievances')
    category = models.ForeignKey(IssueCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='assigned_grievances')
    resolution_details = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=grievance_image_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
        ],
        help_text="Upload image in JPG, JPEG, PNG or GIF format"
    )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def clean(self):
        """Custom validation"""
        if self.status == 'RESOLVED' and not self.resolution_details:
            raise ValidationError("Resolution details are required when marking as resolved")

    def save(self, *args, **kwargs):
        """Custom save with validation"""
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
        ]
