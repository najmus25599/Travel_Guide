from django import forms
from . import models

class UserProfile(forms.ModelForm):
    class Meta:
        model = models.userProfile
        fields = ['user_name', 'user_phone', 'user_address', 'bio', 'user_image']

class HotelReview(forms.ModelForm):
    class Meta:
        model = models.HotelReview
        fields = ['name', 'hotelName', 'review', 'rating']

class chatForm(forms.ModelForm):
    class Meta:
        model = models.chat
        fields = ['to_user', 'chat']

class chatForumForm(forms.ModelForm):
    class Meta:
        model = models.chatForumMessages
        fields = ['message']

class wishlistForm(forms.ModelForm):
    class Meta:
        model = models.wishlist
        fields = ['PlaceName']