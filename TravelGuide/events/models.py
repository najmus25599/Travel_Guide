from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings


class Location(models.Model):
    spot = models.CharField(max_length=120)

    def __str__(self):
        return self.spot


class Transport(models.Model):
    vehicle = models.CharField(max_length=120)

    def __str__(self):
        return self.vehicle


class Stuff(models.Model):
    stuff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    des = models.CharField(max_length=120, default='Stuff')


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=120, default='event-slug', unique=True)
    date = models.DateTimeField(editable=True, blank=True, null=True)
    price = models.FloatField(max_length=None, editable=True, default=0.0)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    stuffs = models.ManyToManyField(Stuff, blank=True)
    capacity = models.IntegerField(default=0)
    location = models.ManyToManyField(Location, blank=False)
    duration_day = models.IntegerField(default=1)
    duration_night = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    transport = models.ManyToManyField(Transport)
    event_img = models.ImageField(upload_to='events/static/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    category_choice = [('bs', 'Business'), ('rx', 'Relax'), ('wd','Wild'), ('mx', 'Mixed'), ('in', 'International')]
    category = models.CharField(max_length=120, choices=category_choice, default='mx')
    objects: models.Manager()




class Enrollment(models.Model):
    enrollment_no = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    traveller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11, blank=False)
    adult = models.IntegerField(default=1, editable=True)
    child = models.IntegerField(default=0)
    paid = models.BooleanField(default=False, editable=True)
    get_discount = models.FloatField(default=0.0, editable=True)
    _msg = models.TextField(blank=True)
    status_choice = [('pending', 'pending'), ('approved', 'approved')]
    status = models.CharField(max_length=120, choices=status_choice, default='pd', editable=True)
    objects: models.Manager()

    def __int__(self):
        return self.enrollment_no


class Review(models.Model):
    op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    star = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], editable=True)
    body = models.TextField(blank=True, editable=True)
    date_posted = models.DateTimeField(auto_now_add=True, editable=False)
    objects: models.Manager()




