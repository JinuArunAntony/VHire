
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, CompanyRegistrationForm
from .models import MenuItem

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        company_form = CompanyRegistrationForm(request.POST)
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()
            company = company_form.save(commit=False)
            company.user = user
            company.save()
            login(request, user)
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        company_form = CompanyRegistrationForm()
    return render(request, 'registration.html', {'user_form': user_form, 'company_form': company_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    print("hi")
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
