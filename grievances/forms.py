from django import forms
from .models import Grievance, IssueCategory

from accounts.models import CustomUser

class GrievanceForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=IssueCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a category",
        required=True
    )
    
    class Meta:
        model = Grievance
        fields = ['category', 'title', 'description', 'location', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name != 'category':  # We already styled category
                field.widget.attrs['class'] = 'form-control'

class GrievanceAdminForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_superuser=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Grievance
        fields = ['status', 'assigned_to', 'resolution_details', 'image']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'resolution_details': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Enter resolution details when marking as resolved'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove these lines - we're not modifying title/description/location anymore
        # if self.instance.pk:
        #     self.fields['title'].required = False
        #     self.fields['description'].required = False
        #     self.fields['location'].required = False
        
        # Only require resolution details when status is being set to RESOLVED
        if self.instance.status != 'RESOLVED':
            self.fields['resolution_details'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('status') == 'RESOLVED' and not cleaned_data.get('resolution_details'):
            self.add_error('resolution_details', "Resolution details are required when marking as resolved")
        return cleaned_data