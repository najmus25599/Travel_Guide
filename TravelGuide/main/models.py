from django.conf import settings
from django.db import models

# Create your models here.

RATE_CHOICES = [
    (1, '1 - Trash'),
    (2, '2- Horrible'),
    (3, '3- Terrible'),
    (4, '4- Bad'),
    (5, '5- OK'),
    (6, '6- Rideable'),
    (7, '7- Good'),
    (8, '8- Very good'),
    (9, '9- Perfect'),
    (10, '10- Best'),

]

PlaceChoices = [
    ('Dhaka', 'Dhaka'),
    ('Barisal', 'Barisal'),
    ('Cumilla', 'Cumilla'),
    ('Cox_Bazar', 'Cox-Bazar'),
    ('Rangamati', 'Rangamati'),
    ('Bandarban', 'Bandarban'),
    ('Khagrachori', 'Khagrachori'),
    ('Moynamoti', 'Moynamoti'),
    ('Sylhet', 'Sylhet'),
    ('Gazipur', 'Gazipur'),
    ('Rajshahi', 'Rajshahi')
]

HotelChoices = [
    ('Pan_Pacific_Sonargoan', 'Pan Pacific Sonargoan'),
    ('Radisson_Blu', 'Radisson Blu'),
    ('Hotel_De_Meridian', 'Hotel De Meridian'),
    ('Grand_Plaza_Hotel', 'Grand Plaza Hotel'),
    ('Empyrean_Hotel', 'Empyrean Hotel'),
    ('The_Raintree_Dhaka', 'The Raintree Dhaka')
]

class userProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=300, null=True)
    user_phone = models.CharField(max_length=20, null=True)
    user_address = models.CharField(max_length=20, null=True)
    date = models.DateTimeField(auto_now_add=True)
    bio = models.CharField(max_length=300, null=True)
    user_image = models.ImageField(blank=True, null=True, upload_to='media', default='user.png')

class RoomModel(models.Model):
    roomtype = models.CharField(max_length=20)
    beds = models.CharField(max_length=20)
    baths = models.CharField(max_length=20)
    slug = models.SlugField()
    guests = models.IntegerField()
    amenities = models.TextField(max_length=3000, blank=True)
    facilities = models.TextField(max_length=3000, blank=True)
    room_Img1 = models.ImageField(blank=True, null=True)
    room_Img2 = models.ImageField(blank=True, null=True)
    room_Img3 = models.ImageField(blank=True, null=True)

class HotelReview(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    hotelName = models.CharField(choices=HotelChoices, max_length=100, default=None, null=True)
    review = models.TextField(max_length=3000, blank=True)
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class HotelReservation(models.Model):
    user_name = models.CharField(max_length=20)
    user_email = models.CharField(max_length=30)
    user_phone = models.CharField(max_length=20)
    checkin_date = models.CharField(max_length=20)
    checkout_date = models.CharField(max_length=20)
    hotelName = models.CharField(choices=HotelChoices, max_length=100, default=None, null=True)
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.DO_NOTHING)

class chat(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.DO_NOTHING, related_name='from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.DO_NOTHING, related_name='to_user')
    chat = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=True)

class chatForumMessages(models.Model):
    message_user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=True)

class wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.DO_NOTHING)
    PlaceName = models.CharField(choices=PlaceChoices, max_length=100, default=None, null=True, unique=True)
    date = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    message = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name