from django import forms
from company.models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'address', 'website', 'contact_number']