from django import forms
from .models import Opportunity, Application, OpportunityCategory

class OpportunityForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=OpportunityCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a category",
        required=True
    )
    
    class Meta:
        model = Opportunity
        fields = ['title', 'description', 'opportunity_type', 'category', 
                 'application_deadline', 'location', 'requirements']
        widgets = {
            'application_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
            'requirements': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
            'opportunity_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the queryset is always fresh
        self.fields['category'].queryset = OpportunityCategory.objects.all()

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message', 'resume']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }