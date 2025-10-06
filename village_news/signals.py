from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Announcement, UserAlert

User = get_user_model()

@receiver(post_save, sender=Announcement)
def create_alerts_for_important_announcements(sender, instance, created, **kwargs):
    if created and instance.is_important and instance.posted_by.is_superuser:
        # Create alerts for all non-superuser users
        for user in User.objects.filter(is_superuser=False):
            UserAlert.objects.get_or_create(user=user, announcement=instance)