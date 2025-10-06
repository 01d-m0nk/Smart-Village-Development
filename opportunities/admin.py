from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Opportunity, Application, OpportunityCategory

@admin.register(OpportunityCategory)
class OpportunityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'opportunity_type', 'category', 'posted_by', 'posted_at', 'is_active')
    list_filter = ('opportunity_type', 'category', 'is_active')
    search_fields = ('title', 'description')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'applicant', 'applied_at', 'status')
    list_filter = ('status', 'opportunity__opportunity_type')
    search_fields = ('opportunity__title', 'applicant__username')