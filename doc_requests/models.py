from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class DocumentRequest(models.Model):
    admin = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_requests'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    document_name = models.CharField(max_length=100, default='Unspecified Document')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

class DocumentSubmission(models.Model):
    request = models.OneToOneField(DocumentRequest, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='user_documents/')
    submitted_at = models.DateTimeField(auto_now_add=True)