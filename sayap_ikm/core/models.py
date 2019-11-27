from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Company(models.Model):
    owners = models.ManyToManyField(User, related_name='companies')
    name = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    image = models.ImageField(null=True)
    prospectus = models.FileField(null=True)
    n_shares = models.PositiveIntegerField(default=0)


class Project(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    prospectus = models.FileField(null=True)
    target = models.PositiveIntegerField(default=0)
    image = models.ImageField(null=True)


class Report(models.Model):
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, related_name='reports')
    description = models.TextField(blank=True, default='')
    file = models.FileField(null=True)
    revenue = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    loan = models.PositiveIntegerField(default=0)
    documentation = models.ImageField(null=True)


class Invest(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='investments')
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, related_name='investments')
    amount = models.PositiveIntegerField(default=0)


class Yield(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='yields')
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, related_name='yields')
    amount = models.PositiveIntegerField(default=0)


class Hold(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='holds')
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, related_name='holds')
    amount = models.PositiveIntegerField(default=0)