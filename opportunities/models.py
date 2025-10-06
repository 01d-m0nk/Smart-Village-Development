from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'opportunities':
        default_categories = [
            ("Government Job", "Government sector employment opportunities"),
            ("Private Job", "Private company employment"),
            ("Vocational Training", "Skill development programs"),
            ("Internship", "Temporary work experience opportunities"),
            ("Freelance", "Project-based work opportunities"),
        ]
        
        for name, description in default_categories:
            OpportunityCategory.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )

class OpportunityCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Opportunity(models.Model):
    OPPORTUNITY_TYPES = [
        ('JOB', 'Job'),
        ('TRAINING', 'Skill Training'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPES)
    category = models.ForeignKey(OpportunityCategory, on_delete=models.SET_NULL, null=True)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posted_opportunities')
    posted_at = models.DateTimeField(default=timezone.now)
    application_deadline = models.DateTimeField()
    location = models.CharField(max_length=200)
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.get_opportunity_type_display()})"

class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('REVIEWED', 'Reviewed'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_applications')
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    message = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"{self.applicant.username} - {self.opportunity.title}"