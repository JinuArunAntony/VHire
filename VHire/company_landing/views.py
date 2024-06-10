from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from company.models import Company
from .forms import CompanyForm


# Create your views here.
def home(request):
    return render(request, 'company_landing_home.html')


@login_required
def company_profile(request):
    company = get_object_or_404(Company, user=request.user)
    return render(request, 'company_profile.html', {'company': company})

@login_required
def edit_company_profile(request):
    company = get_object_or_404(Company, user=request.user)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_landing:company_profile')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'edit_company_profile.html', {'form': form})
   
