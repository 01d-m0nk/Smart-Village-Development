from django import forms
from .models import Poll, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'active', 'show_results']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3}),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'placeholder': 'Add choice'}),
        }

ChoiceFormSet = forms.inlineformset_factory(
    Poll, Choice, form=ChoiceForm,
    extra=2, can_delete=False, min_num=2, validate_min=True
)