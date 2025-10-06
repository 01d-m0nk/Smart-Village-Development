from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

User = get_user_model()

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('POWER', 'Power Cut Information'),
        ('EVENT', 'Village Events'),
        ('HEALTH', 'Health Camps'),
        ('GENERAL', 'General Announcements'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_important = models.BooleanField(default=False)
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('village_news:announcement_detail', kwargs={'pk': self.pk})

class UserAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'announcement')
    
    def __str__(self):
        return f"{self.user.username} - {self.announcement.title}"