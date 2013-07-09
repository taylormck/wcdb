from django.db import models

# Create your models here.

class CommonType(models.Model):
    summary = models.TextField('Summary')
    
class ListType(models.Model):
    href = models.TextField('href')
    embed = models.TextField('embed')
    text = models.TextField('text')

class Crisis(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    kind = models.CharField('Kind', max_length=255)
    date = models.DateField('Date')
    time = models.TimeField('Time')
    name = models.CharField('Name', max_length=100)
    common = CommonType('Common')
    people = models.ManyToManyField('Person', verbose_name='Associated people')
    organizations = models.ManyToManyField('Organization', verbose_name='Associated organizations')

class Organization(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    kind = models.CharField('Kind', max_length=255)
    location = models.CharField('Location', max_length=255)
    name = models.CharField('Name', max_length=100)
    history = ListType('History')
    contactInfo = ListType('Contact Info')
    common = CommonType('Common')
    people = models.ManyToManyField('Person', verbose_name='Associated people')

class Person(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField('Name', max_length=100)
    kind = models.CharField('Kind', max_length=255)
    location = models.CharField('Location', max_length=255)
    common = CommonType('Common')

"""
# These are all the types of List Types
class Location(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class HumanImpact(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class EconomicImpact(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class ResourcesNeeded(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class WaysToHelp(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class Citations(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class ExternalLinks(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class Images(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class Videos(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class Maps(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)

class Feeds(ListType):
    crisis = models.ForeignKey('Crisis', Crisis)
"""
