from django.urls import path
from company_landing.views import home
from company_landing import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'company_landing'


urlpatterns = [
    
    path('home/',views.home, name='home'),
    path('profile/', views.company_profile, name='company_profile'),
    path('edit/', views.edit_company_profile, name='edit_company_profile'),
    path('jobs/', views.add_job_with_candidate, name='add_job_with_candidate'),
    path('all_jobs/', views.all_jobs, name='all_jobs'),
    path('job_with_candidates_success/<int:job_id>/', views.job_with_candidates_success, name='job_with_candidates_success'),
    path('candidates/',views.all_candidates,name='all_candidates'),
    path('all_jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('all_jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('candidates/edit/<int:candidate_id>/', views.edit_candidate, name='edit_candidate'),
    path('candidates/delete/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('add_candidate/', views.add_candidate, name='add_candidate'),
     

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
