from django.db import models

# Create your models here.

class Common(models.Model):
    summary = models.TextField('Summary')
    
class ListType(models.Model):
    href = models.TextField('href')
    embed = models.TextField('embed')
    altText = models.TextField('altText')
    text = models.TextField('text')
    
    class Meta:
        abstract = True

class Crisis(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    kind = models.CharField('Kind', max_length=255)
    date = models.DateField('Date', null=True)
    time = models.TimeField('Time', null=True)
    name = models.CharField('Name', max_length=100)
    common = models.OneToOneField('Common')
    people = models.ManyToManyField('Person', verbose_name='Associated people')
    organizations = models.ManyToManyField('Organization', verbose_name='Associated organizations')

class Organization(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    kind = models.CharField('Kind', max_length=255)
    location = models.CharField('Location', max_length=255)
    name = models.CharField('Name', max_length=100)
    history = ListType('History')
    contactInfo = ListType('Contact Info')
    common = models.OneToOneField('Common')
    people = models.ManyToManyField('Person', verbose_name='Associated people')

class Person(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField('Name', max_length=100)
    kind = models.CharField('Kind', max_length=255)
    location = models.CharField('Location', max_length=255)
    common = models.OneToOneField('Common')


# These are all the types of List Types
class CommonListType(ListType):
    CITATIONS = 'CI'
    EXTERNAL_LINKS = "EL"
    IMAGES = 'IM'
    VIDEOS = 'VI'
    MAPS = 'MA'
    FEEDS = 'FE'
    
    LIST_TYPE_CHOICES = (
        (CITATIONS, 'Citations'),
        (EXTERNAL_LINKS, 'External Links'),
        (IMAGES, 'Images'),
        (VIDEOS, 'Videos'),
        (MAPS, 'Maps'),
        (FEEDS, 'Feeds'),
    )
    
    context = models.CharField(max_length=2,choices=LIST_TYPE_CHOICES,default=EXTERNAL_LINKS)
    owner = models.ForeignKey('Common')
    

#Below are exclusive to crisis
class CrisisListType(ListType):
    LOCATION = 'LO'
    HUMAN_IMPACT = 'HI'
    ECONOMIC_IMPACT = 'EI'
    RESOURCES_NEEDED = 'RN'
    WAYS_TO_HELP = 'WH'
    
    LIST_TYPE_CHOICES = (
        (LOCATION, 'Location'),
        (HUMAN_IMPACT, 'Human Impact'),
        (ECONOMIC_IMPACT, 'Economic Impact'),
        (RESOURCES_NEEDED,'Resources Needed'),
        (WAYS_TO_HELP,'Ways To Help'),
    )
    
    context = models.CharField(max_length=2,choices=LIST_TYPE_CHOICES,default=LOCATION)
    owner = models.ForeignKey('Crisis')

