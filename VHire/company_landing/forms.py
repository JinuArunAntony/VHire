from django import forms
from company.models import Company
from .models import Job, Candidate
from django.forms import inlineformset_factory


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'address', 'website', 'contact_number']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name','last_name', 'email', 'resume']


CandidateFormSet = inlineformset_factory(Job, Candidate, form=CandidateForm, extra=1)