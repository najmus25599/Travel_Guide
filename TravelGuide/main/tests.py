from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from main.forms import HotelReview

from main.models import RoomModel, userProfile, HotelReservation

from main.views import index, UserProfile, createProfile, about, RoomShow, hotel_page, \
    hotelReview, deleteHotelReview, hotel_bookingPdf, reservationnew, hotelsearch, \
    directmessage, sentmessage,contact, chatForum, wishList, usersearch, searcheduser

from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class UrlsTest(SimpleTestCase):

    def test_index(self):
        url = reverse('main:base_template')
        self.assertEquals(resolve(url).func, index)

    def test_UserProfile(self):
        url = reverse('main:user_profile')
        self.assertEquals(resolve(url).func, UserProfile)

    def test_createProfile(self):
        url = reverse('main:create_profile')
        self.assertEquals(resolve(url).func, createProfile)

    def test_about(self):
        url = reverse('main:about')
        self.assertEquals(resolve(url).func, about)

    def test_contact(self):
        url = reverse('main:contact')
        self.assertEquals(resolve(url).func, contact)

    def test_hotelReview(self):
        url = reverse('main:hotelReview')
        self.assertEquals(resolve(url).func, hotelReview)

    def test_hotel_bookingPdf(self):
        url = reverse('main:hotel_bookingPdf')
        self.assertEquals(resolve(url).func, hotel_bookingPdf)

    def test_RoomShow(self):
        url = reverse('main:hotel_page')
        self.assertEquals(resolve(url).func, hotel_page)

    def test_hotel_page(self):
        url = reverse('main:RoomShow')
        self.assertEquals(resolve(url).func, RoomShow)

    def test_reservationnew(self):
        url = reverse('main:reservation_new')
        self.assertEquals(resolve(url).func, reservationnew)

    def test_directmessage(self):
        url = reverse('main:direct_message')
        self.assertEquals(resolve(url).func, directmessage)

    def test_sentmessage(self):
        url = reverse('main:sent_message')
        self.assertEquals(resolve(url).func, sentmessage)

    def test_chatForum(self):
        url = reverse('main:chat_forum')
        self.assertEquals(resolve(url).func, chatForum)

    def test_wishList(self):
        url = reverse('main:wishlist')
        self.assertEquals(resolve(url).func, wishList)

    def test_usersearch(self):
        url = reverse('main:usersearch')
        self.assertEquals(resolve(url).func, usersearch)

    def test_searcheduser(self):
        url = reverse('main:searcheduser')
        self.assertEquals(resolve(url).func, searcheduser)


class ViewTest(TestCase):
    def test_index(self):
        response = self.client.get(reverse('main:base_template'))
        self.assertEquals(response.status_code, 200)
    def test_about(self):
        response = self.client.get(reverse('main:about'))
        self.assertEquals(response.status_code, 200)

    def test_contact(self):
        response = self.client.get(reverse('main:contact'))
        self.assertEquals(response.status_code, 200)

    def test_hotelReview(self):
        response = self.client.post(reverse('main:hotelReview'))
        self.assertEquals(response.status_code, 302)

    def test_deleteHotelReview(self):
        response = self.client.post(reverse('main:deleteHotelReview', args=['slug']))
        self.assertEquals(response.status_code, 302)

    def test_hotel_bookingPdf(self):
        response = self.client.post(reverse('main:hotel_bookingPdf'))
        self.assertEquals(response.status_code, 302)

    def test_RoomShow(self):
        response = self.client.post(reverse('main:RoomShow'))
        self.assertEquals(response.status_code, 302)

    def test_hotel_page(self):
        response = self.client.post(reverse('main:hotel_page'))
        self.assertEquals(response.status_code, 302)

    def test_chatForum(self):
        response = self.client.post(reverse('main:chat_forum'))
        self.assertEquals(response.status_code, 302)

    def test_wishList(self):
        response = self.client.post(reverse('main:wishlist'))
        self.assertEquals(response.status_code, 302)

    def test_usersearch(self):
        response = self.client.post(reverse('main:usersearch'))
        self.assertEquals(response.status_code, 302)

    def test_searcheduser(self):
        response = self.client.post(reverse('main:searcheduser'))
        self.assertEquals(response.status_code, 302)

class TestModels(TestCase):
        def test_RoomModel(self):
            self.roomModel = RoomModel.objects.create(
                roomtype='test room',
                beds='test bed',
                baths='test bath',
                slug='test_slug',
                guests=10,
                amenities='test amenities',
                facilities='test facilities'
            )
            self.assertEquals(self.roomModel.roomtype, 'test room')
            self.assertEquals(self.roomModel.beds, 'test bed')
            self.assertEquals(self.roomModel.baths, 'test bath')
            self.assertEquals(self.roomModel.slug, 'test_slug')
            self.assertEquals(self.roomModel.guests, 10)
            self.assertEquals(self.roomModel.amenities, 'test amenities')
            self.assertEquals(self.roomModel.facilities, 'test facilities')

        def test_userProfile(self):
            self.userProfile = userProfile.objects.create(
                user_name='test user_name',
                user_phone='test user_phone',
                user_address='test user_address',
                bio='test bio'
            )
            self.assertEquals(self.userProfile.user_name, 'test user_name')
            self.assertEquals(self.userProfile.user_phone, 'test user_phone')
            self.assertEquals(self.userProfile.user_address, 'test user_address')
            self.assertEquals(self.userProfile.bio, 'test bio')


class TestForms(SimpleTestCase):
    def test_HotelReview_Form_Valid_Data(self):
        form = HotelReview(data={
            'name': 'test name',
            'hotelName': 'Radisson_Blu',
            'review': 'test review',
            'rating': 10
        })

        self.assertTrue(form.is_valid())

    def test_HotelReview_Form_no_data(self):
        form = HotelReview(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)




