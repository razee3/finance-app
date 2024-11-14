from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['income_categories', 'expense_categories']
        widgets = {
            'income_categories': forms.Textarea(attrs={'placeholder': 'Enter income categories, separated by commas', 'style': 'width: 400px; height: 100px;'}),
            'expense_categories': forms.Textarea(attrs={'placeholder': 'Enter expense categories, separated by commas', 'style': 'width: 400px; height: 100px;'}),
        }