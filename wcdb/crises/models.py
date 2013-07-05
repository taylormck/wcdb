from django.db import models

# Create your models here.
class Crisis(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField('Name', max_length=100)
    date = models.DateField('Date')
    info = models.TextField('About')
    people = models.ManyToManyField('Associated people', Person)
    organizations = models.ManyToManyField('Associated organizations', Organization)

class Organization(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField('Name', max_length=100)
    info = models.TextField('About')
    people = models.ManyToManyField('Associated people', Person)

class Person(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField('Name', max_length=100)
    birth = models.DateField('Date of birth')
    death = models.DateField('Date of death', blank=True, null=True)
    info = models.TextField('About')