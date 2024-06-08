from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('company_name', 'address', 'website', 'contact_number')
