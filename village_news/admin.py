

# Register your models here.
from django.contrib import admin
from .models import Announcement, UserAlert

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted_by', 'created_at', 'is_important')
    list_filter = ('category', 'is_important', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set posted_by if creating new
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(UserAlert)