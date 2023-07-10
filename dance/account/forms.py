from profile import Profile
from django import forms
from django.contrib.auth.models import User
from .models import Profile

ROLE_CHOICES = (('TEACHER', 'Teacher'), ('STUDENT', 'Student'))

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)
    role = forms.ChoiceField(label='What is your role', choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('Email already in use.')
        return email
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Email already in use.')
        return email

class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )

    class Meta:
        model = Profile
        fields = ['photo', 'description','date_of_birth']

