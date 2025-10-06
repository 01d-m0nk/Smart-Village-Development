
# Register your models here.
from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('question', 'created_by__username')
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Vote)