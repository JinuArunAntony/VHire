from django.urls import path
from company_landing.views import home
from company_landing import views
app_name = 'company_landing'

urlpatterns = [
    
    path('home/',home, name='home'),
    path('profile/', views.company_profile, name='company_profile'),
    path('edit/', views.edit_company_profile, name='edit_company_profile'),
    
     

]