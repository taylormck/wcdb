from django.db import models

# Create your models here.
class Crisis(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    kind = models.CharField('Kind')
    date = models.DateField('Date')
    time = models.TimeField('Time')
    name = models.CharField('Name', max_length=100)
    common = CommonType('Common')
    people = models.ManyToManyField('Associated people', Person)
    organizations = models.ManyToManyField('Associated organizations', Organization)

class Organization(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    kind = models.CharField('Kind')
    location = models.CharField('Location')
    name = models.CharField('Name', max_length=100)
    history = ListType('History')
    contactInfo = ListType('Contact Info')
    common = CommonType('Common')
    people = models.ManyToManyField('Associated people', Person)

class Person(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField('Name', max_length=100)
    kind = models.CharField('Kind')
    location = models.CharField('Location')
    birth = models.DateField('Date of birth')
    death = models.DateField('Date of death', blank=True, null=True)
    common = CommonType('Common')

class ListType(models.Model):
    href = models.CharField('href')
    embed = models.CharField('embed')
    text = models.TextField('text')

class CommonType(models.Model):
    summary = models.TextField('Summary')

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
