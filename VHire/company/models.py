from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    website = models.URLField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.company_name
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name
