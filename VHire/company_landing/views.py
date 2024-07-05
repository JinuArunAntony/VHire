from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from company.models import Company
from .models import Job, Candidate
from .forms import CompanyForm,JobForm, CandidateFormSet,CandidateForm
from django.forms import modelformset_factory
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Candidate
from django.conf import settings
from django.forms import formset_factory
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q



# Create your views here.
def home(request):
    return render(request, 'company_landing_home.html')


def all_candidates(request):
    return render(request,'all_candidates.html')

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




@login_required
def add_job_with_candidate(request):
    if request.method == 'POST':
        job_form = JobForm(request.POST)
        candidate_forms = [CandidateForm(request.POST, request.FILES, prefix=str(i)) for i in range(int(request.POST.get('form-TOTAL_FORMS')))]
        candidate_credentials = []

        if job_form.is_valid():
            job = job_form.save(commit=False)  # Use commit=False here
            job.company = request.user.company
            job.save()

            for form in candidate_forms:
                if form.is_valid():
                    candidate = form.save(commit=False)
                    username = f"{candidate.first_name.lower()}.{candidate.last_name.lower()}"
                    user_count = User.objects.filter(username__startswith=username).count()
                    if user_count > 0:
                        username += str(user_count + 1)
                    password = User.objects.make_random_password()
                    vhire_user = User.objects.create_user(username=username, password=password)
                    candidate.user = vhire_user
                    candidate.job = job
                    candidate.company = job.company
                    candidate.save()
                    candidate_credentials.append({
                        'first_name': candidate.first_name,
                        'last_name': candidate.last_name,
                        'email': candidate.email,
                        'username': username,
                        'password': password
                    })

            request.session['candidate_credentials'] = candidate_credentials
            return redirect('company_landing:job_with_candidates_success', job_id=job.id)
    else:
        job_form = JobForm()
        candidate_forms = [CandidateForm(prefix=str(i)) for i in range(1)]
        empty_candidate_form = CandidateForm(prefix='_prefix_')

    return render(request, 'add_job_with_candidate.html', {
        'job_form': job_form,
        'candidate_forms': candidate_forms,
        'empty_candidate_form': empty_candidate_form,
    })
@login_required
def job_with_candidates_success(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    candidate_credentials = request.session.pop('candidate_credentials', [])

    return render(request, 'job_with_candidates_success.html', {
        'job': job,
        'candidate_credentials': candidate_credentials
    })
@login_required
def all_jobs(request):
    user = request.user
    if hasattr(user, 'company'):
        company = user.company
        query = request.GET.get('q')
        if query:
            jobs = Job.objects.filter(company=company, title__icontains=query)
        else:
            jobs = Job.objects.filter(company=company)
        job_candidates = {job.id: job.candidate_set.all() for job in jobs}
        return render(request, 'all_jobs.html', {'jobs': jobs, 'job_candidates': job_candidates, 'query': query})
    else:
        return render(request, 'all_jobs.html', {'jobs': [], 'job_candidates': {}, 'query': ''})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('all_jobs')
    else:
        form = JobForm(instance=job)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'form': form.as_p()})
    return render(request, 'all_jobs.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('company_landing:all_jobs')
    return render(request, 'company_landing/all_jobs.html')

@login_required
def edit_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, user_id=candidate_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('all_jobs')
    else:
        form = CandidateForm(instance=candidate)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'form': form.as_p()})
    return render(request, 'all_jobs.html')

@login_required
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, user_id=candidate_id)
    if request.method == 'POST':
        candidate.delete()
        return redirect('company_landing:all_jobs')
    return render(request, 'company_landing/all_jobs.html')
@login_required
def all_candidates(request):
    query = request.GET.get('q')
    if query:
        candidates = Candidate.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        candidates = Candidate.objects.all()
    
    return render(request, 'all_candidates.html', {'candidates': candidates, 'query': query})

@login_required
def add_candidate(request, job_id=None):
    user = request.user
    if hasattr(user, 'company'):
        company = user.company
        job = get_object_or_404(Job, id=job_id, company=company) if job_id else None

        if request.method == 'POST':
            formset = CandidateFormSet(request.POST, request.FILES, instance=job)
            if formset.is_valid():
                formset.save()
                return redirect('add_candidate', job_id=job.id)
        else:
            formset = CandidateFormSet(instance=job)
        
        return render(request, 'add_candidate.html', {'job': job, 'formset': formset, 'jobs': Job.objects.filter(company=company)})
    else:
        return render(request, 'add_candidate.html', {'job': None, 'formset': None, 'jobs': []})