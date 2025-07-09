from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
# Create your models here.
from django.db.models import IntegerField



class Buses(models.Model):
    name = models.CharField(max_length=1020)
    seat = models.IntegerField(default=40)
    category_choice = [('ac', 'AC'),('nonac','Non AC'),('Sleeper','Sleeper')]
    type = models.CharField(max_length=120,choices=category_choice)
    slug = models.SlugField(max_length=120,default="slug",editable=True)
    objects: models.Manager()

    def __str__(self):
        return self.name

class Schedule(models.Model):
    bus=models.ForeignKey(Buses,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    fair=models.FloatField(default=500.0)
    slug = models.SlugField(default="slug")
    category_choice = [('ac', 'AC'),('nonac','Non AC'),('Sleeper','Sleeper')]

    type = models.CharField(max_length=120,choices=category_choice,default='nonac')
    available=IntegerField(default=44,editable=True)
    object: models.Manager()
    def __str__(self):
        return self.bus.name


class Book(models.Model):
    bus=models.ForeignKey(Schedule,on_delete=models.CASCADE)
    booker=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    passenger=models.IntegerField(default=1)
    fair=models.FloatField(default=0.0)
    date=models.DateField(auto_now_add=True)
    object: models.Manager()