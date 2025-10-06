from django import forms
from .models import DocumentRequest, DocumentSubmission

class RequestDocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ['user', 'document_name']

class SubmitDocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentSubmission
        fields = ['document_file']