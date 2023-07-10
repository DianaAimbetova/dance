from django import forms
from .models import Class

class ClassEnrollForm(forms.Form):
 course = forms.ModelChoiceField(
 queryset=Class.objects.all(),
 widget=forms.HiddenInput)

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        exclude = ['teacher',
                   'slug',
                    'created',
                    'students']
        
        widgets = {
            'planned_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
