from django.urls import path
from company.views import register, login_view,home
from django.contrib.auth.views import LogoutView

app_name = 'company'

urlpatterns = [
    path('',home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]