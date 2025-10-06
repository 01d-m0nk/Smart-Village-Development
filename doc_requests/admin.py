from django.contrib import admin
from .models import DocumentRequest, DocumentSubmission

class DocumentSubmissionInline(admin.TabularInline):
    model = DocumentSubmission
    extra = 0

@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_name', 'is_completed')
    inlines = [DocumentSubmissionInline]